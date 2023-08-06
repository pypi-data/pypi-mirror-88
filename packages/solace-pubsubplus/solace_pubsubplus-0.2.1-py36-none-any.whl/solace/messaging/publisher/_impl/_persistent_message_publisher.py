# pubsubplus-python-client
#
# Copyright 2020 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module contains the implementation class and methods for the PersistentMessagePublisher"""
# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-ancestors,protected-access
# pylint: disable=missing-function-docstring, unused-variable,no-else-break,no-else-return,no-else-continue
import logging
import queue
import threading
import time
from typing import Union, Any, Dict

from solace.messaging import SolaceServiceAdapter
from solace.messaging.config._sol_constants import SOLCLIENT_DELIVERY_MODE_PERSISTENT, SOLCLIENT_DELIVERY_MODE_DIRECT
from solace.messaging.config._solace_message_constants import VALUE_CANNOT_BE_NEGATIVE, \
    DELIVERY_LISTENER_SERVICE_DOWN_EXIT_MESSAGE, GRACE_PERIOD_MAX_MS, \
    UNABLE_TO_SET_LISTENER, PUBLISH_TIME_OUT, \
    UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER, INVALID_ADDITIONAL_PROPS
from solace.messaging.core import _solace_session
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, PubSubTimeoutError, \
    IllegalArgumentError, IncompleteMessageDeliveryError, IllegalStateError
from solace.messaging.publisher._impl._message_publisher import _MessagePublisher, _MessagePublisherState
from solace.messaging.publisher._impl._outbound_message import _OutboundMessage
from solace.messaging.publisher._impl._publisher_utilities import _PublisherUtilities
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.persistent_message_publisher import PersistentMessagePublisher, MessageDeliveryListener
from solace.messaging.resources.topic import Topic
from solace.messaging.utils._solace_utilities import _Util

logger = logging.getLogger('solace.messaging.publisher')


class PersistentDeliveryListenerThread(threading.Thread) \
        :  # pylint: disable=too-few-public-methods, missing-class-docstring
    #  Thread to let the callback know about readiness of direct message publisher when is actually ready.

    def __init__(self, persistent_publisher, message_handler, stop_event, persistent_ack_queue,
                 message_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_info = f"PersistentDeliveryListenerThread Id: {str(hex(id(self)))}"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] initialized', type(self).__name__)
        self._persistent_publisher = persistent_publisher
        self._persistent_ack_queue = persistent_ack_queue
        self._message_delivery_listener_handler = message_handler
        self._stop_event = stop_event
        self._delivery_receipt_empty = persistent_publisher.delivery_receipt_empty
        self._correlation = persistent_publisher.correlation
        self._messaging_service = message_service

    @property
    def listener(self):
        return self._message_delivery_listener_handler

    @listener.setter
    def listener(self, handler):
        self._message_delivery_listener_handler = handler

    def run(self):
        # run method will listen to the ack event and prepare the delivery receipt and hook it to
        # the message handler for every acked message from the queue
        while not self._stop_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session._MessagingServiceState.DOWN:
                # call the publisher's terminate method to ensure proper cleanup of thread
                self.adapter.warning(DELIVERY_LISTENER_SERVICE_DOWN_EXIT_MESSAGE)
                break
            else:
                if not self._persistent_publisher.can_listen_to_ack_event.is_set() and \
                        self._persistent_ack_queue.qsize() == 0 \
                        and not self._persistent_publisher.asked_to_terminate:
                    self._persistent_publisher.can_listen_to_ack_event.wait()
                # don't attempt to deliver the delivery receipt  when we are  terminating
                if self._persistent_ack_queue.qsize() > 0 and not self._delivery_receipt_empty.is_set():
                    _, exception = self._persistent_ack_queue.get()
                    outbound_message, persisted, timestamp, user_context = \
                        self._persistent_publisher.prepare_delivery_receipt()
                    delivery_receipt = DeliveryReceipt(outbound_message, exception, timestamp, persisted, user_context)
                    if not any([outbound_message, persisted, timestamp, user_context]):
                        continue
                    else:
                        try:
                            self._message_delivery_listener_handler.on_delivery_receipt(delivery_receipt)
                        except PubSubPlusClientError as exception:
                            self.adapter.warning("Failed to dispatch. Message handler type: [%s]. "
                                                 "Exception: %s",
                                                 type(self._message_delivery_listener_handler),
                                                 str(exception))
                if self._persistent_ack_queue.qsize() == 0 \
                        and not self._persistent_publisher.asked_to_terminate:
                    # let the thread wait for can_listen_to_ack event
                    self._persistent_publisher.can_listen_to_ack_event.clear()

                # when ack buffer is empty &  correlation list is empty
                # while we  are at terminating state we are signalling main thread
                # to wake up to proceed to clean up
                if self._persistent_ack_queue.qsize() == 0 and \
                        self._persistent_publisher.asked_to_terminate and \
                        not self._delivery_receipt_empty.is_set() and len(self._correlation) == 0:
                    self._delivery_receipt_empty.set()


class _PersistentMessagePublisher(_MessagePublisher, PersistentMessagePublisher) \
        :  # pylint: disable=too-many-instance-attributes, too-many-ancestors
    # implementation class for persistent message publisher

    def __init__(self, persistent_message_publisher):
        super().__init__(persistent_message_publisher, SOLCLIENT_DELIVERY_MODE_PERSISTENT)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)
        self._persistent_message_publisher = persistent_message_publisher
        self._pub_id = ("publish_" + str(hex(id(self)))).encode()
        self._pub_await_ack_id = ("publish_await_acknowledgement_" + str(hex(id(self)))).encode()
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized with pub_id [%s] and pub_await_id [%s]',
                               type(self).__name__, self._pub_id, self._pub_await_ack_id)
        self._can_listen_to_ack_event = self._persistent_message_publisher.messaging_service.api.can_listen_to_ack
        # dynamically we are creating an queue(method name+ object id)
        # for each publisher's publish & publish await acknowledge in SolaceApi class
        self._persistent_ack_queue = queue.Queue()
        setattr(self._persistent_message_publisher.messaging_service.api,
                self._pub_id.decode(), self._persistent_ack_queue)

        self._persistent_await_ack_queue = queue.Queue()
        setattr(self._persistent_message_publisher.messaging_service.api,
                self._pub_await_ack_id.decode(),
                self._persistent_await_ack_queue)

        self._delivery_listener = None
        self._delivery_listener_thread = None
        self._delivery_listener_thread_stop_event = threading.Event()
        self._message_publisher_state = _MessagePublisherState.NOT_STARTED
        self._delivery_mode = SOLCLIENT_DELIVERY_MODE_PERSISTENT
        self._correlation = list()  # maintains the  msg_p & its user_context

    @property
    def correlation(self):
        return self._correlation

    @property
    def delivery_receipt_empty(self):
        return self._delivery_receipt_empty

    @property
    def can_listen_to_ack_event(self):
        # property to hold and return the can listen event for acknowledgement"""
        return self._can_listen_to_ack_event

    def set_message_delivery_listener(self, listener: 'MessageDeliveryListener'):
        # Method for setting the message delivery listener"""
        _Util.is_type_matches(listener, MessageDeliveryListener, logger=logger)
        if self._message_publisher_state in [_MessagePublisherState.STARTED, _MessagePublisherState.READY]:
            self._delivery_listener = listener
            if self._delivery_listener_thread is None:
                self._delivery_listener_thread = \
                    PersistentDeliveryListenerThread(self, self._delivery_listener,
                                                     self._delivery_listener_thread_stop_event,
                                                     self._persistent_ack_queue,
                                                     self._messaging_service)
                self._delivery_listener_thread.daemon = True
                self._delivery_listener_thread.start()
            else:
                self._delivery_listener_thread.listener = listener
            return self
        else:
            error_message = f'{UNABLE_TO_SET_LISTENER}. Message Publisher is NOT started/ready'
            self.adapter.warning(error_message)
            raise IllegalStateError(error_message)

    def publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic, user_context: Any = None,
                additional_message_properties: Dict[str, Union[str, int, bytearray]] = None):
        # Sends message to the given destination
        _PublisherUtilities.validate_topic_type(destination=destination, logger=logger)
        if additional_message_properties:
            _Util.is_none_or_empty_exists(additional_message_properties,
                                          error_message=INVALID_ADDITIONAL_PROPS, logger=logger)
        self.__do_publish(message, destination, additional_message_properties, correlation_tag=self._pub_id)
        self._correlation.append((self._message.solace_message, user_context))

    def publish_await_acknowledgement(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                                      time_out: int = None,
                                      additional_message_properties: Dict[str, Union[str, int, bytearray]] = None):
        # Sends OutboundMessage to the given destination, blocking until delivery acknowledgement is received or timeout
        # occurs
        #
        # :py:class:`~solace.messaging.builder.direct_message_publisher_builder.DirectMessagePublisherBuilder`
        #  can be used to create the OutboundMessage instance.  Alternatively, a bytearray or string payload may be
        #  passed to publish() and the API will create a py:class:`~solace.messaging.core.message.Message` to send.
        #
        # Args:
        #     message ():   py:class:`~solace.messaging.core.message.Message` or payload to publish
        #     destination (): Destination to add to the message
        #     time_out (:obj:`int`, optional):  max time in ms to wait for the message acknowledgement
        #     additional_message_properties (Dict[str, Union[str, int, bytearray]]):additional properties,
        #     to customize a particular message, each key can be customer provided, or it can be a key from a
        #     :py:mod:`~solace.messaging.config.solace_properties.message_properties`, The value can be either a string
        #      or an integer or a bytearray
        #
        # Returns:
        #
        # Raises:
        # PubSubTimeoutError:  is thrown after specified timeout when no response received
        # MessageRejectedByBrokerError: when message was rejected from a broker for some reason
        # PublisherOverflowError: when publisher publishes too fast, application may attempt to
        # republish the message.
        # MessageDestinationDoesNotExistError: given message destination does not exist
        # IllegalArgumentError: if the value of timeout is negative or invalid
        _PublisherUtilities.validate_topic_type(destination=destination, logger=logger)
        if time_out is not None and time_out < 0:
            raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
        self.__do_publish(message, destination, additional_message_properties,
                          correlation_tag=self._pub_await_ack_id)
        try:
            timeout_in_seconds = _Util.convert_ms_to_seconds(time_out) if time_out is not None else None
            event, exception = self._persistent_await_ack_queue.get(True, timeout=timeout_in_seconds)
            if exception:
                raise exception
        except queue.Empty as exception:
            raise PubSubTimeoutError(PUBLISH_TIME_OUT) from exception

    def terminate_now(self):
        if not self._is_publisher_available_for_terminate():
            return

        with self._terminate_now_lock:
            if not self._is_publisher_available_for_terminate():
                return

            self._message_publisher_state = _MessagePublisherState.TERMINATING
            self._can_listen_to_ack_event.set()  # wake up delivery listener thread
            self._asked_to_terminate = True  # flag to prevent the thread to sleep while terminating
            self._handle_events_on_terminate()

            self._cleanup()
            self._queues_cleanup()

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # start = datetime.datetime.now()
        #
        # print("called terminate", self._message_publisher_buffer_queue.qsize(),  flush=True)
        _Util.validate_grace_period_min(grace_period=grace_period, logger=logger)
        if not self._is_publisher_available_for_terminate():
            return
        # print("before acquiring lock")
        with self._terminate_lock:
            # print("after  acquiring lock")
            # Even after acquiring lock still we have to check the state, since state can be modified by other threads
            if not self._is_publisher_available_for_terminate():
                return

            self._message_publisher_state = _MessagePublisherState.TERMINATING
            self._can_listen_to_ack_event.set()  # wake up delivery listener thread
            self._asked_to_terminate = True  # flag to prevent the thread to sleep while terminating
            self._handle_events_on_terminate()

            grace_period_in_seconds = _Util.convert_ms_to_seconds(grace_period)

            # print("gonna wait for publisher thread")
            remaining_time = self._wait_on_publisher_thread(timeout=grace_period_in_seconds)
            # print("remaining time", remaining_time)
            timeout = remaining_time if self._message_publisher_thread else grace_period_in_seconds
            self._wait_on_delivery_listener_thread(timeout)
            # print("gonna do cleanups")
            self._cleanup()
            self._queues_cleanup()
        # print("finally in have done",  self.d)

    def prepare_delivery_receipt(self):
        # Method for preparing the delivery receipt
        if self._correlation:
            solace_message, user_context = self._correlation.pop(0)  # The oldest message is always ack first so first
            # item will be popped here
            outbound_message = _OutboundMessage(solace_message)
            delivery_mode = outbound_message.solace_message.get_delivery_mode()
            is_persisted = delivery_mode != SOLCLIENT_DELIVERY_MODE_DIRECT
            return outbound_message, is_persisted, time.time(), user_context
        else:
            return None, None, None, None

    def _cleanup(self):
        self._asked_to_terminate = True
        # Method stops the publisher thread
        super()._cleanup()
        # remove publisher queue from internal solace session
        sol_api = self._messaging_service.api
        setattr(sol_api, self._pub_id.decode(), None)

        setattr(sol_api, self._pub_await_ack_id.decode(), None)
        self._delivery_listener_thread_stop_event.set()
        self._can_listen_to_ack_event.set()
        if self._delivery_listener_thread is not None:
            self._delivery_listener_thread.join()
        self._message_publisher_state = _MessagePublisherState.TERMINATED

    def _queues_cleanup(self):
        if self._message_publisher_buffer_queue is not None and self._message_publisher_buffer_queue.qsize() != 0:
            error_message = f"{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER}. " \
                            f"Unpublished message count: [{self._message_publisher_buffer_queue.qsize()}]. " \
                            f"Undelivered delivery receipt count: [{self._persistent_await_ack_queue.qsize()}]"
            self.adapter.warning(error_message)
            # if start:
            #     print((datetime.datetime.now()- start).total_seconds())
            #     print(self.d)
            #     print("buff size", self._message_publisher_buffer_queue.qsize() )
            self._message_publisher_buffer_queue = None
            self._persistent_await_ack_queue = None
            self._correlation.clear()
            raise IncompleteMessageDeliveryError(error_message)

    def __do_publish(self, message, destination, additional_message_properties, correlation_tag):
        # Implementation method for publishing a message
        return super().message_publish(message, destination,
                                       additional_message_properties=
                                       additional_message_properties,
                                       correlation_tag=correlation_tag)


class DeliveryReceipt:
    """
    Encapsulates broker acknowledgement or failed publishing attempt details, used for message
    delivery notification processing such as timestamp, correlation token, original message,
    indicator if message was persisted on a broker, exception if any.
    """

    def __init__(self, message: OutboundMessage, exception: PubSubPlusClientError, time_stamp: int,
                 persisted: bool, user_context: object = None):
        self._message: OutboundMessage = message
        self._exception: PubSubPlusClientError = exception
        self._time_stamp: int = time_stamp
        self._persisted: bool = persisted
        self._user_context: object = user_context

    @property
    def user_context(self) -> object:
        """Retrieve the context associated with an action if provided during publishing

        Returns:
            context associated with broker delivery confirmation action or null if there is none.
        """
        return self._user_context

    @property
    def time_stamp(self) -> int:
        """
        Retrieves the timestamp, number of ms from the epoch of 1970-01-01T00:00:00Z

        Returns:
            int value of the timestamp
        """
        return self._time_stamp

    @property
    def message(self) -> OutboundMessage:
        """
        Retrieves message associated with a Receipt

        Returns:
            message associated with this instance of the Receipt
        """
        return self._message

    @property
    def exception(self) -> PubSubPlusClientError:
        """
        Gets exception if any, indicating failure case

        Returns:
            non null value indicates failure by delivery to the broker or during persistence on a broker
        """
        return self._exception

    @property
    def is_persisted(self) -> bool:
        """
        Gets information if message reached a broker and persistence confirmation was received back

        Returns:
            true if broker confirmed that message is received and persisted, false otherwise
        """
        return self._persisted

    def __str__(self):
        return f"message : {str(self._message)} time_stamp : {str(self._time_stamp)} " \
               f"exception : {str(self._exception)} persisted : {str(self._persisted)} "
