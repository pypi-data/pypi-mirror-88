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

"""Module contains the implementation cass and methods for the DirectMessageReceiver"""
# pylint: disable=too-many-ancestors, too-many-instance-attributes, missing-class-docstring, missing-function-docstring
# pylint: disable=no-else-break,no-else-return,inconsistent-return-statements,protected-access

import concurrent
import copy
import logging
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from ctypes import Structure, c_int, c_uint32, c_void_p, py_object, CFUNCTYPE
from typing import Union

from solace.messaging import SolaceServiceAdapter
from solace.messaging.config._sol_constants import SOLCLIENT_CALLBACK_TAKE_MSG, SOLCLIENT_OK
from solace.messaging.config._solace_message_constants import UNABLE_TO_RECEIVE_MESSAGE_RECEIVER_NOT_STARTED, \
    RECEIVER_TERMINATED, UNABLE_TO_UNSUBSCRIBE_TO_TOPIC, DISPATCH_FAILED, \
    RECEIVER_SERVICE_DOWN_EXIT_MESSAGE, GRACE_PERIOD_MAX_MS, \
    RECEIVER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED, RECEIVE_MESSAGE_FROM_BUFFER
from solace.messaging.core import _solace_session
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, IllegalStateError
from solace.messaging.receiver._impl._inbound_message import _InboundMessage
from solace.messaging.receiver._impl._message_receiver import _MessageReceiver, _MessageReceiverState
from solace.messaging.receiver._impl._receiver_utilities import _ReceiverUtilities
from solace.messaging.receiver._inbound_message_utility import topic_subscribe_with_dispatch, \
    topic_unsubscribe_with_dispatch
from solace.messaging.receiver.direct_message_receiver import DirectMessageReceiver
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.utils._solace_utilities import _Util

logger = logging.getLogger('solace.messaging.receiver')


class _DirectMessageReceiverThread(threading.Thread):  # pylint: disable=missing-class-docstring
    # Thread used to dispatch received messages on a receiver.

    def __init__(self, direct_message_receiver, messaging_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_info = f"_DirectMessageReceiverThread Id: {str(hex(id(self)))}"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_receiver = direct_message_receiver
        self._message_receiver_queue = self._message_receiver.receiver_queue
        self._message_handler = None
        self._stop_event = self._message_receiver.stop_event  # we receive this from direct message impl class
        self._can_receive_event = self._message_receiver.can_receive_event
        self._receiver_empty_event = self._message_receiver.receiver_empty_event
        self._messaging_service = messaging_service

    @property
    def message_handler(self):
        return self._message_handler

    @message_handler.setter
    def message_handler(self, message_handler):
        self._message_handler = message_handler

    def run(self):  # pylint: disable=missing-function-docstring
        # Start running thread
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] started', type(self).__name__)
        while not self._stop_event.is_set():
            # stop the thread only when the internal buffer is empty to ensure the delivery of all messages
            # when service is down
            if self._messaging_service.api.message_service_state == _solace_session._MessagingServiceState.DOWN and \
                    self._message_receiver_queue.qsize() == 0:
                # call the receiver's terminate method to ensure proper cleanup of thread
                self.adapter.warning("%s", RECEIVER_SERVICE_DOWN_EXIT_MESSAGE)
                if self._message_receiver.asked_to_terminate:
                    self._message_receiver.receiver_empty_event.set()  # wakeup main thread when the service is down
                break
            else:
                if not self._can_receive_event.is_set() and \
                        not self._message_receiver.asked_to_terminate:
                    self._can_receive_event.wait()
                # don't attempt to retrieve message once buffer is declared as empty  at terminating
                # state( there is a chance we may keep receiving message callback which are in transit)
                if self._message_receiver_queue.qsize() > 0 and not \
                        self._message_receiver.receiver_empty_event.is_set():
                    inbound_message = self._message_receiver_queue.get()
                    if inbound_message:
                        try:
                            self._message_handler.on_message(inbound_message)
                        except Exception as exception:  # pylint: disable=broad-except
                            self.adapter.warning("%s %s", DISPATCH_FAILED, str(exception))

                # don't block the thread at terminating state
                elif not self._message_receiver.asked_to_terminate:
                    self._can_receive_event.clear()

                if self._message_receiver_queue.qsize() == 0 and \
                        self._message_receiver.asked_to_terminate and \
                        not self._message_receiver.receiver_empty_event.is_set():
                    # let the main thread stop waiting in terminating state
                    self._message_receiver.receiver_empty_event.set()


class _DirectMessageReceiver(_MessageReceiver, DirectMessageReceiver):
    # class for direct message receiver, it is the base class used to receive direct messages

    class SolClientReceiverCreateRxMsgDispatchFuncInfo(Structure) \
            :  # pylint: disable=too-few-public-methods, missing-class-docstring
        # Conforms to solClient_session_rxMsgDispatchFuncInfo

        _fields_ = [
            ("dispatch_type", c_uint32),  # The type of dispatch described
            ("callback_p", CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)),  # An application-defined callback
            # function; may be NULL if there is no callback.
            ("user_p", py_object),  # A user pointer to return with the callback; must be NULL if callback_p is NULL.
            ("rffu", c_void_p)  # Reserved for Future use; must be NULL
        ]

    def __init__(self, messaging_service, config):  # pylint: disable=duplicate-code
        super().__init__(messaging_service)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)
        self._running = False

        self._message_handler = None
        self._can_receive_event = threading.Event()
        self._can_receive_id = "can_receive_" + str(hex(id(self)))
        setattr(self._messaging_service.api,
                self._can_receive_id, self._can_receive_event)
        self._messaging_service.api.can_receive.append(self._can_receive_id)
        self._direct_message_receiver_thread = None
        self._direct_message_receiver_thread_stop_event = threading.Event()
        self._msg_callback_func_routine = self.msg_callback_func_type(self.__message_receive_callback_routine)
        self._topic_dict = {}
        self._group_name = None
        self._receiver_empty_event = threading.Event()
        self._is_unsubscribed = False
        key = "subscriptions"
        if key in config:
            subscription = config[key]
            if isinstance(subscription, str):
                self._topic_dict[subscription] = False  # not applied
            else:
                for topic in subscription:
                    self._topic_dict[topic] = False  # not applied
        key = "group_name"
        if key in config:
            self._group_name = config[key]
        self._message_receiver_state = _MessageReceiverState.NOT_STARTED

    def __unsubscribe(self):  # pylint: disable=duplicate-code
        # called as part of terminate
        if self._is_unsubscribed:
            return
        if self._topic_dict and self._messaging_service.is_connected:
            self._is_unsubscribed = True
            topics = [*copy.deepcopy(self._topic_dict)]
            # unsubscribe topics as part of teardown activity
            for topic in topics:
                try:
                    self.__do_unsubscribe(topic)
                except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenarios
                    self.adapter.warning(exception)

    def _cleanup(self):
        self._asked_to_terminate = True  # flag to prevent  the thread to sleep while terminating
        self._message_receiver_state = _MessageReceiverState.TERMINATED
        if self._direct_message_receiver_thread is not None:
            # set thread termination flag before waking delivery thread
            # to ensure clean exit from python message delivery thread
            self._direct_message_receiver_thread_stop_event.set()

            self._can_receive_event.set()  # don't block the thread while terminating
            # wake message delivery thread
            # join on python message delivery thread
            self._direct_message_receiver_thread.join()

    def __is_receiver_started(self) -> bool:
        # Method to validate receiver is properly started or not"""
        _, self._message_receiver_state = \
            _ReceiverUtilities.is_message_service_connected(receiver_state=self._message_receiver_state,
                                                            message_service=self._messaging_service,
                                                            logger=logger)
        if self._message_receiver_state == _MessageReceiverState.NOT_STARTED or \
                self._message_receiver_state == _MessageReceiverState.STARTING:
            raise IllegalStateError(UNABLE_TO_RECEIVE_MESSAGE_RECEIVER_NOT_STARTED)
        if self._message_receiver_state == _MessageReceiverState.TERMINATING or \
                self._message_receiver_state == _MessageReceiverState.TERMINATED:
            raise IllegalStateError(RECEIVER_TERMINATED)
        if self._message_receiver_state != _MessageReceiverState.STARTED:
            raise IllegalStateError(UNABLE_TO_RECEIVE_MESSAGE_RECEIVER_NOT_STARTED)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] %s', DirectMessageReceiver.__name__, _MessageReceiverState.STARTED.name)
        return True

    def __do_start(self):
        # start the DirectMessageReceiver (always blocking).
        errors = None
        for topic, subscribed in self._topic_dict.items():
            if not subscribed:
                try:
                    self.add_subscription(TopicSubscription.of(topic))
                    self._topic_dict[topic] = True
                except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenarios
                    errors = str(exception) if errors is None else errors + "; " + str(exception)
                    self._message_receiver_state = _MessageReceiverState.NOT_STARTED
                    self.adapter.warning("%s %s", RECEIVER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED,
                                         str(errors))
                    raise PubSubPlusClientError \
                        (message=f"{RECEIVER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED}{str(errors)}") from exception
                    # pragma: no cover # Due to core error scenarios
        self._running = True
        self._message_receiver_state = _MessageReceiverState.STARTED
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('%s is %s', DirectMessageReceiver.__name__, _MessageReceiverState.STARTED.name)

    def __do_subscribe(self, topic_subscription: str):
        # Subscribe to a topic (always blocking).
        if self._group_name is None or self._group_name == '':
            subscribe_to = topic_subscription
        else:
            subscribe_to = "#share/" + self._group_name + "/" + topic_subscription
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('SUBSCRIBE to: [%s]', subscribe_to)

        dispatch_info = self.SolClientReceiverCreateRxMsgDispatchFuncInfo(
            c_uint32(1),
            self._msg_callback_func_routine,
            py_object(self),
            c_void_p(None))

        return_code = topic_subscribe_with_dispatch(self._messaging_service.session_pointer,
                                                    subscribe_to, dispatch_info)
        if return_code == SOLCLIENT_OK:
            self._topic_dict[topic_subscription] = True
        else:
            failure_message = f'{UNABLE_TO_UNSUBSCRIBE_TO_TOPIC} [{topic_subscription}].'
            last_error = _Util.get_last_error_info(return_code=return_code,
                                                   caller_description='_DirectMessageReceiver->__do_subscribe',
                                                   exception_message=failure_message)
            self.adapter.warning('%s. Status code: %d. %s', failure_message, return_code,
                                 last_error)  # pragma: no cover # Due to core error scenarios
            raise PubSubPlusClientError(message=f'{failure_message}. '
                                                f'Status code: {return_code}')  # pragma: no cover

    def __do_unsubscribe(self, topic_subscription: str):
        # Unsubscribe from a topic (always blocking).
        if self._group_name is None or self._group_name == '':
            unsubscribe_to = topic_subscription
        else:
            unsubscribe_to = "#share/" + self._group_name + "/" + topic_subscription
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('UNSUBSCRIBE to: [%s]', unsubscribe_to)
        dispatch_info = self.SolClientReceiverCreateRxMsgDispatchFuncInfo(c_uint32(1), self._msg_callback_func_routine,
                                                                          py_object(self), c_void_p(None))

        return_code = topic_unsubscribe_with_dispatch(self._messaging_service.session_pointer, unsubscribe_to,
                                                      dispatch_info)
        if topic_subscription in self._topic_dict:
            del self._topic_dict[topic_subscription]
        if return_code != SOLCLIENT_OK:
            failure_message = f'{UNABLE_TO_UNSUBSCRIBE_TO_TOPIC} [{unsubscribe_to}].'
            last_error_info = _Util.get_last_error_info(return_code=return_code,
                                                        caller_description='_DirectMessageReceiver->__do_unsubscribe',
                                                        exception_message=failure_message)
            self.adapter.warning("%s", last_error_info)
            raise PubSubPlusClientError(last_error_info)

    def __message_receive_callback_routine(self, opaque_session_p, msg_p, user_p) \
            :  # pragma: no cover  # pylint: disable=unused-argument
        # The message callback is invoked for each Direct message received by the Session
        try:
            solace_message = _SolaceMessage(c_void_p(msg_p))
            rx_msg = _InboundMessage(solace_message)
            self._message_receiver_queue.put(rx_msg)
            self._can_receive_event.set()
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('PUT message to %s buffer/queue', DirectMessageReceiver.__name__)
        except Exception as exception:
            self.adapter.error(exception)
            raise PubSubPlusClientError(message=exception) from exception
        return SOLCLIENT_CALLBACK_TAKE_MSG  # we took the received message

    @property
    def receiver_state(self):
        return self._message_receiver_state

    @property
    def receiver_queue(self):
        return self._message_receiver_queue

    @property
    def stop_event(self):  # pylint: disable=duplicate-code
        return self._direct_message_receiver_thread_stop_event

    @property
    def can_receive_event(self):  # pylint: disable=duplicate-code
        return self._can_receive_event

    @property
    def receiver_empty_event(self):
        return self._receiver_empty_event

    def start(self) -> DirectMessageReceiver:
        # Start the DirectMessageReceiver synchronously (blocking).
        # return self if we already started the receiver
        if self._message_receiver_state == _MessageReceiverState.STARTED:
            return self

        with self._start_lock:
            super().start()
            # Even after acquiring lock still we have to check the state to avoid re-doing the work
            if self._message_receiver_state == _MessageReceiverState.STARTED:
                return self

            elif self._message_receiver_state == _MessageReceiverState.NOT_STARTED:
                self._message_receiver_state = _MessageReceiverState.STARTING
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug(' [%s] is %s', DirectMessageReceiver.__name__,
                                       _MessageReceiverState.STARTING.name)
                _, self._message_receiver_state = \
                    _ReceiverUtilities.is_message_service_connected(receiver_state=self._message_receiver_state,
                                                                    message_service=self._messaging_service,
                                                                    logger=logger)
                self.__do_start()
                return self

    def add_subscription(self, another_subscription: TopicSubscription):
        # Subscribe to a topic synchronously (blocking). """
        _ReceiverUtilities.validate_subscription_type(subscription=another_subscription, logger=logger)
        self._can_add_subscription()
        self.__do_subscribe(another_subscription.get_name())

    def add_subscription_async(self, topic_subscription: TopicSubscription) -> concurrent.futures.Future:
        # method to add the subscription asynchronously
        _ReceiverUtilities.validate_subscription_type(topic_subscription)
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.add_subscription, topic_subscription)

    def receive_message(self, timeout: int = None) -> Union[InboundMessage, None]:
        # Get a message, blocking for the time configured in the receiver builder. """
        self._can_receive_message()
        if timeout is not None:
            _Util.is_not_negative(input_value=timeout, logger=logger)

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug("%s", RECEIVE_MESSAGE_FROM_BUFFER)
        if timeout:  # used in deciding whether to put None in queue or not when flow goes down
            self._messaging_service.api.receiver_queues.append(self._message_receiver_queue)  # used to unblock
        try:
            message = self._message_receiver_queue.get(block=bool(timeout),
                                                       timeout=_Util.convert_ms_to_seconds(
                                                           timeout) if timeout else None)
            self._check_buffer()
            return message
        except queue.Empty:  # when timeout arg is given just return None on timeout
            return
        except (PubSubPlusClientError, KeyboardInterrupt) as exception:
            raise exception

    def receive_async(self, message_handler: MessageHandler):
        # Specify the asynchronous message handler.
        _Util.is_type_matches(actual=message_handler, expected_type=MessageHandler, logger=logger)
        with self._receive_lock:
            self._can_receive_message()
            if self._direct_message_receiver_thread is None:
                self._direct_message_receiver_thread = _DirectMessageReceiverThread(self, self._messaging_service)
                self._direct_message_receiver_thread.message_handler = message_handler
                self._direct_message_receiver_thread.daemon = True
                self._direct_message_receiver_thread.start()
            else:  # just update the thread's message handler
                self._direct_message_receiver_thread.message_handler = message_handler
            return self

    def remove_subscription(self, subscription: TopicSubscription):
        # Unsubscribe from a topic synchronously (blocking).
        _ReceiverUtilities.validate_subscription_type(subscription=subscription, logger=logger)
        self._can_remove_subscription()
        self.__do_unsubscribe(subscription.get_name())

    def remove_subscription_async(self, topic_subscription: TopicSubscription) -> concurrent.futures.Future:
        # method to remove the subscription asynchronously
        _ReceiverUtilities.validate_subscription_type(topic_subscription)
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.remove_subscription, topic_subscription)

    def terminate_now(self):
        super().terminate_now()
        with self._terminate_now_lock:
            if not self._is_receiver_available_for_terminate():
                return
            self._message_receiver_state = _MessageReceiverState.TERMINATING
            self.__unsubscribe()
            self._handle_events_on_terminate()
            self._cleanup()
            self._check_undelivered_messages()
            self.adapter.info("%s", RECEIVER_TERMINATED)

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # Stop the receiver - put None in the queue which will stop our asynchronous
        #             dispatch thread, or the app will get if it asks for another message via sync.
        super().terminate()
        with self._terminate_lock:
            if not self._is_receiver_available_for_terminate():
                return
            self._message_receiver_state = _MessageReceiverState.TERMINATING
            self._asked_to_terminate = True  # flag to prevent  the thread to sleep while terminating
            grace_period_in_seconds = _Util.convert_ms_to_seconds(grace_period)
            self.__unsubscribe()
            self._handle_events_on_terminate()
            if self._direct_message_receiver_thread:
                self._receiver_empty_event.wait(timeout=grace_period_in_seconds)
            self._cleanup()
            self._check_undelivered_messages()
            self.adapter.info("%s", RECEIVER_TERMINATED)
