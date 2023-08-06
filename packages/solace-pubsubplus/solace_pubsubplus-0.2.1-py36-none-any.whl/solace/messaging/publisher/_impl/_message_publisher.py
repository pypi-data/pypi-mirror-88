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

# Module contains the implementation class and methods for the MessagePublisher
# pylint: disable=missing-module-docstring, too-many-branches,no-else-break,too-many-boolean-expressions,R1710
# pylint: disable=missing-function-docstring,protected-access,no-else-raise,no-else-return

import concurrent
import datetime
import enum
import logging
import queue
import threading
import typing
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

from solace.messaging import SolaceServiceAdapter
from solace.messaging.config._sol_constants import SOLCLIENT_WOULD_BLOCK, SOLCLIENT_OK, \
    SOLCLIENT_DELIVERY_MODE_PERSISTENT, SOLCLIENT_DELIVERY_MODE_DIRECT
from solace.messaging.config._solace_message_constants import UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED, \
    PUBLISHER_TERMINATED, WOULD_BLOCK_EXCEPTION_MESSAGE, PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED, \
    PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED, QUEUE_FULL_EXCEPTION_MESSAGE, \
    UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER, UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING, \
    PUBLISHER_READINESS_SERVICE_DOWN_EXIT_MESSAGE, UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY, \
    PUBLISHER_SERVICE_DOWN_EXIT_MESSAGE, MESSAGING_SERVICE_DOWN, GRACE_PERIOD_MAX_MS, \
    UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED, PUBLISHER_ALREADY_TERMINATED, \
    PUBLISHER_TERMINATED_UNABLE_TO_START, PUBLISHER_UNAVAILABLE_FOR_TERMINATE
from solace.messaging.config.publisher_back_pressure_configuration import PublisherBackPressure
from solace.messaging.core import _solace_session
from solace.messaging.core._publish import _SolacePublish
from solace.messaging.errors.pubsubplus_client_error import IllegalStateError, PublisherOverflowError, \
    InvalidDataTypeError, PubSubPlusClientError, IncompleteMessageDeliveryError
from solace.messaging.publisher._impl import _direct_message_publisher
from solace.messaging.publisher._impl._outbound_message import _OutboundMessageBuilder
from solace.messaging.publisher._impl._publisher_utilities import _PublisherUtilities
from solace.messaging.publisher._outbound_message_utility import add_message_properties, set_correlation_tag_ptr
from solace.messaging.publisher._publishable import Publishable
from solace.messaging.publisher.message_publisher import MessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.publisher_health_check import PublisherReadinessListener
from solace.messaging.resources.topic import Topic
from solace.messaging.utils._solace_utilities import _Util

logger = logging.getLogger('solace.messaging.publisher')


class _MessagePublisherState(enum.Enum):  # pylint: disable=too-few-public-methods,missing-class-docstring
    # Enum class for defining the message publisher state
    NOT_STARTED = 0
    STARTING = 1
    STARTED = 2
    TERMINATING = 3
    TERMINATED = 4
    NOT_READY = 5
    READY = 6


class PublisherReadinessListenerThread(threading.Thread) \
        :  # pylint: disable=too-few-public-methods, missing-class-docstring, missing-function-docstring
    # Thread to let the callback know about readiness of direct message publisher when is actually ready.

    def __init__(self, message_publisher: 'MessagePublisher', messaging_service: 'MessagingService', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_info = f"PublisherReadinessListenerThread Id: {str(hex(id(self)))}"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_publisher: 'MessagePublisher' = message_publisher
        self._publisher_readiness_listener = message_publisher.listener
        self._stop_listening_event = message_publisher.publisher_readiness_listener_thread_stop_event
        self._messaging_service: 'MessagingService' = messaging_service

    def run(self):
        # Start running thread
        # to INVOKE callback is being SET in SET_PUBLISHER_READINESS_LISTENER.
        # WOULD_BLOCK event should have occurred in API while direct PUBLISHing message AND
        # at the same time API will emit CAN_SEND_RECEIVED AND IS_READY method should return TRUE,
        # meanwhile notification SHOULDN'T BE SENT already
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] started', type(self).__name__)
        while not self._stop_listening_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session._MessagingServiceState.DOWN:
                # call the publisher's terminate method to ensure proper cleanup of thread
                self.adapter.warning(PUBLISHER_READINESS_SERVICE_DOWN_EXIT_MESSAGE)
                break
            while not self._messaging_service.api.can_send_received.is_set():
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug('THREAD: [%s] is waiting for CAN_SEND event', type(self).__name__)
                self._messaging_service.api.can_send_received.wait()

            if self._message_publisher.is_ready() and \
                    not self._message_publisher.is_publisher_readiness_listener_notification_sent:
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug('IS_READY: True. Invoking [%s]', type(self).__name__)
                self._publisher_readiness_listener.ready()
                self._message_publisher.is_publisher_readiness_listener_notification_sent = True
                self._message_publisher.would_block_received.clear()


class MessagePublisherThread(threading.Thread):  # pylint: disable=missing-class-docstring, too-many-instance-attributes
    # Message publisher thread

    def __init__(self, message_publisher, messaging_service, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._id_info = f"MessagePublisherThread Id: {str(hex(id(self)))}"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_publisher = message_publisher
        self._publisher_buffer_queue = message_publisher.message_publisher_buffer_queue
        self._publisher_thread_stop_event = message_publisher.publisher_thread_stop_event
        self._publisher_thread_can_peek_buffer_event = message_publisher.can_peek_buffer_event
        self._retry_count = 0
        self._messaging_service = messaging_service
        self._publisher_empty = message_publisher.publisher_empty

    def run(self):  # pylint: disable= missing-function-docstring
        # Start running thread when
        # Publisher buffer/queue should not be empty and WOULD_BLOCK SESSION event not happened,
        # if WOULD_BLOCK received, ensure it receives CAN_SEND SESSION event received
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('THREAD: [%s] started', type(self).__name__)
        while not self._publisher_thread_stop_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session._MessagingServiceState.DOWN:
                # notify about the publish failure only in direct mode
                if self._message_publisher.delivery_mode == SOLCLIENT_DELIVERY_MODE_DIRECT:
                    while True:
                        try:
                            element: tuple = self._publisher_buffer_queue.get_nowait()
                            self._message_publisher.notify_publish_error(
                                PubSubPlusClientError(MESSAGING_SERVICE_DOWN),
                                element[1].get_message(),
                                element[1].get_destination())
                        except queue.Empty:
                            break
                if self._message_publisher.asked_to_terminate:
                    self._publisher_empty.set()  # wakeup main thread when the service is down while terminating
                # call the publisher's terminate method to ensure proper cleanup of thread
                self.adapter.warning("%s", PUBLISHER_SERVICE_DOWN_EXIT_MESSAGE)
                break
            else:
                if not self._message_publisher.asked_to_terminate and \
                        not self._publisher_thread_can_peek_buffer_event.is_set() and \
                        self._publisher_buffer_queue.qsize() == 0:
                    self._publisher_thread_can_peek_buffer_event.wait()
                # don't attempt to publish  when we are  terminating
                if (not self._message_publisher.would_block_received.is_set()
                    and self._publisher_buffer_queue.qsize() > 0) \
                        or (self._message_publisher.would_block_received.is_set()
                            and self._messaging_service.api.can_send_received.is_set()
                            and self._publisher_buffer_queue.qsize() > 0) and not self._publisher_empty.is_set():
                    message_publisher, publishable = self._publisher_buffer_queue.queue[0]
                    self._publish(message_publisher, publishable)

                elif self._message_publisher.would_block_received.is_set() and \
                        not self._messaging_service.api.can_send_received.is_set():
                    if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                        self.adapter.debug('THREAD: [%s] is waiting for CAN_SEND event', type(self).__name__)
                    # if self._message_publisher._message_publisher_state == _MessagePublisherState.TERMINATING:
                    #     print("im waiting", self._messaging_service.api.can_send_received.is_set())
                    self._messaging_service.api.can_send_received.wait()
                    # if self._message_publisher._message_publisher_state == _MessagePublisherState.TERMINATING:
                    #     print("wake up now")
                if self._publisher_buffer_queue.qsize() == 0 and not self._message_publisher.asked_to_terminate:
                    # let the thread wait for can_peek event
                    self._publisher_thread_can_peek_buffer_event.clear()
                # signaling that message publisher buffer is empty and can proceed to clean-up
                elif self._message_publisher.asked_to_terminate and \
                        self._publisher_buffer_queue.qsize() == 0 and not self._publisher_empty.is_set():
                    self._publisher_empty.set()

    def _publish(self, message_publisher: 'MessagePublisher', publishable: 'TopicPublishable'):
        try:
            status_code = message_publisher.do_publish(publishable)
            if status_code == SOLCLIENT_OK:
                self._publisher_buffer_queue.get_nowait()
            elif status_code == SOLCLIENT_WOULD_BLOCK:
                self._retry_count += 1
        except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenarios
            self.adapter.error('%s', str(exception))


class _MessagePublisher(MessagePublisher) \
        :  # pylint: disable=R0904, missing-function-docstring, too-many-instance-attributes, missing-class-docstring

    # implementation class for message publisher

    def __init__(self, message_publisher: Union['_DirectMessagePublisherBuilder', '_PersistentMessagePublisherBuilder'],
                 delivery_mode: str):
        # Args:
        #     messaging_service (MessageService):
        #     delivery_mode
        # self.d = {_MessagePublisherState.READY: 0, _MessagePublisherState.STARTED: 0,
        #            _MessagePublisherState.TERMINATING: 0, _MessagePublisherState.TERMINATED: 0}
        # self.count_lock = threading.Lock()
        self._messaging_service: '_BasicMessagingService' = message_publisher.messaging_service
        self._id_info = f"{self._messaging_service.logger_id_info} - " \
                        f"[PUBLISHER: {str(hex(id(self)))}]"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)

        self._delivery_mode = delivery_mode
        self._publisher_back_pressure_type = message_publisher.publisher_back_pressure_type
        self._message_publisher_buffer_queue = None
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            self._message_publisher_buffer_queue = queue.Queue(maxsize=message_publisher.buffer_capacity)
        self._publisher_readiness_listener_thread = None
        self._listener = None
        self._message_publisher_thread = None
        self._message_publisher_state = _MessagePublisherState.NOT_STARTED
        self._is_notified = False
        self._would_block_received = self._messaging_service.api.would_block_received
        self._publishable = None
        self._publisher_thread_stop_event = threading.Event()
        self._outbound_message_builder = _OutboundMessageBuilder()
        self._publisher_readiness_listener_thread_stop_event = threading.Event()
        self._can_peek_buffer_event = threading.Event()
        self._can_peek_id = "can_peek_" + str(hex(id(self)))
        setattr(self._messaging_service.api,
                self._can_peek_id, self._can_peek_buffer_event)
        self._messaging_service.api.can_peek.append(self._can_peek_id)
        self._asked_to_terminate = False
        self._message = None
        self._publisher_empty = threading.Event()  # to signal publisher
        # buffer is empty in terminating state
        self._delivery_receipt_empty = threading.Event()  # to signal delivery receipt listener
        # buffer is empty in terminating state
        self._delivery_listener = None
        self._error_notification_dispatcher: _direct_message_publisher.PublishFailureNotificationDispatcher = \
            _direct_message_publisher.PublishFailureNotificationDispatcher()
        self._start_future = None
        self._terminate_future = None
        self._start_lock = threading.Lock()
        self._start_async_lock = threading.Lock()
        self._terminate_now_lock = threading.Lock()
        self._terminate_lock = threading.Lock()
        self._terminate_async_lock = threading.Lock()
        self._would_block_lock = threading.Lock()
        # self.pub_count = 0

    @property
    def asked_to_terminate(self):
        return self._asked_to_terminate

    @property
    def delivery_mode(self):
        return self._delivery_mode

    @property
    def publisher_empty(self):
        return self._publisher_empty

    @property
    def publisher_thread_stop_event(self):
        # property to hold and return the publisher thread stop event
        return self._publisher_thread_stop_event

    @property
    def publisher_readiness_listener_thread_stop_event(self):
        # property to hold and return the publisher readiness listener thread stop event
        return self._publisher_readiness_listener_thread_stop_event

    @property
    def can_peek_buffer_event(self):
        # property to hold and return the can peek into buffer event
        return self._can_peek_buffer_event

    def is_ready(self) -> bool:
        # Non-blocking check if publisher can potentially publish messages.
        # Returns:
        #     bool: False if MessagePublisher is not STARTED or
        #     MessagePublisher is NOT_READY[WOULD_BLOCK occurred AND CAN_SEND_RECEIVED not SET],
        #     else True and set MessagePublisherState to READY

        if self._message_publisher_state in [_MessagePublisherState.TERMINATED,
                                             self._message_publisher_state == _MessagePublisherState.TERMINATING]:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('[%s] is [%s]. State: [%s]', type(self).__name__,
                                   _MessagePublisherState.NOT_READY.name, self._message_publisher_state.name)
            return False

        # When we have buffer availability when backPressure is ON, then MessagePublisher is READY
        if self._message_publisher_buffer_queue is not None and not self._message_publisher_buffer_queue.full():
            self._message_publisher_state = _MessagePublisherState.READY
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('[%s] is [%s]. MessagePublisher buffer/queue is not full',
                                   type(self).__name__, _MessagePublisherState.READY.name)
            return True

        # if this is MessagePublisher NOT_READY, WOULD_BLOCK should have occurred,
        # so check if CAN_SEND_RECEIVED event is SET
        if self._message_publisher_state == _MessagePublisherState.NOT_READY and \
                self.would_block_received.is_set() and self._messaging_service.api.can_send_received.is_set():
            # WOULD_BLOCK should have occurred, at the same time CAN_SEND_RECEIVED event should be SET,
            # to decide MessagePublisher is READY
            self._message_publisher_state = _MessagePublisherState.READY
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('[%s] is [%s]. CAN_SEND received', type(self).__name__,
                                   _MessagePublisherState.READY.name)
            return True

        # either MessagePublisher should be STARTED or READY and WOULD_BLOCK event should not have occurred
        if (self._message_publisher_state == _MessagePublisherState.STARTED or
            self._message_publisher_state == _MessagePublisherState.READY) and not \
                self.would_block_received.is_set():
            self._message_publisher_state = _MessagePublisherState.READY
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('[%s] is [%s/%s]', type(self).__name__, _MessagePublisherState.READY.name,
                                   _MessagePublisherState.STARTED.name)
            return True

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('status: [%s]. is CAN_SEND SET?: %s', type(self).__name__, self._message_publisher_state,
                               self._messaging_service.api.can_send_received.is_set())
        return False

    def set_publisher_readiness_listener(self, listener: PublisherReadinessListener) -> 'MessagePublisher':
        # Sets a publisher state listener
        # Args:
        #     listener: listener to observe publisher state
        # Returns:
        _Util.is_type_matches(listener, PublisherReadinessListener)
        if self._listener is None:
            self._listener = listener
            if logger.isEnabledFor(logging.DEBUG):
                self.adapter.debug("%s", 'NOTIFICATION SCHEDULED')
            self._publisher_readiness_listener_thread = PublisherReadinessListenerThread(self, self._messaging_service)
            self._publisher_readiness_listener_thread.daemon = True
            self._publisher_readiness_listener_thread.start()
            self.is_publisher_readiness_listener_notification_sent = False

        return self

    def notify_when_ready(self):
        #
        # Non-blocking request to notify PublisherReadinessListener.
        # This method helps to overcome race condition between completion of the exception
        # processing on publishing of 'ready' aka can send event
        # Returns:
        #     None : returns none
        #
        if self._listener is None:
            self.adapter.warning("%s is not set", PublisherReadinessListener)
            raise PubSubPlusClientError(message=f"{PublisherReadinessListener} is not set")
        if self.is_publisher_readiness_listener_notification_sent:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug("%s", 'NOTIFICATION SCHEDULED')
        self.is_publisher_readiness_listener_notification_sent = False

    def start(self):
        if self._message_publisher_state in [_MessagePublisherState.TERMINATING, _MessagePublisherState.TERMINATED]:
            self.adapter.warning("%s", PUBLISHER_TERMINATED_UNABLE_TO_START)
            raise IllegalStateError(PUBLISHER_TERMINATED_UNABLE_TO_START)

        elif self._message_publisher_state == _MessagePublisherState.STARTED:
            return self

        with self._start_lock:
            # Even after acquiring lock still we have to check the state to avoid re-doing the work
            if self._message_publisher_state == _MessagePublisherState.STARTED:
                return self

            if self._message_publisher_state == _MessagePublisherState.NOT_STARTED:
                self._is_message_service_connected()
                self._message_publisher_state = _MessagePublisherState.STARTED
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug('[%s] is %s. Publisher back-pressure Type: %s', type(self).__name__,
                                       _MessagePublisherState.STARTED.name, self._publisher_back_pressure_type)
            return self

    def start_async(self) -> concurrent.futures.Future:
        # Start the Receiver asynchronously (non-blocking)
        if self.__is_connecting() or self.__is_connected():
            return self._start_future
        with self._start_async_lock:
            # Even after acquiring lock still we have to check the state to avoid spinning up the executor
            if self.__is_connecting() or self.__is_connected():
                return self._start_future

            with ThreadPoolExecutor() as executor:
                self._start_future = executor.submit(self.start)
                return self._start_future

    def notify_publish_error(self, exception, message, destination):
        # This method triggers the PublishFailureNotificationDispatcher's on exception method
        #  Args:
        #      exception: exception message stack trace
        #      message: published message
        #      destination: destination topic
        #
        publishable = Publishable.of(message, destination)
        self._error_notification_dispatcher.on_exception(exception_occurred=exception, publishable=publishable)

    def do_publish(self, publishable: 'TopicPublishable'):  # pylint: disable=missing-function-docstring
        # Method to call underlying CORE publish method
        # Args:
        #     publishable (TopicPublishable): TopicPublishable instance contains OutboundMessage & Topic
        # Returns:
        #     publish status code
        try:
            publish_status = _SolacePublish(self._messaging_service).publish(publishable.get_message(),
                                                                             publishable.get_destination())
            if publish_status == SOLCLIENT_OK and not self._messaging_service.api.can_send_received.is_set():
                # print("gonna set can send send in pub 0 status")
                self._messaging_service.api.can_send_received.set()
            # print("pub", publish_status)
            # with self.count_lock:
            #     self.pub_count += 1
            #     self.d[self._message_publisher_state] += 1
            # if self._message_publisher_state == _MessagePublisherState.TERMINATING :
            #     print("pub status", publish_status, flush=True, ) # self._message_publisher_state, publish_status,
            #     self.pub_count, flush=True, )
            # # if self._publisher_back_pressure_type != PublisherBackPressure.No and \
            # #         publish_status == SOLCLIENT_OK and self._would_block_received.is_set():
            # #     # print("gonna clear would block ")
            # #     self._would_block_received.clear()
            if self._delivery_mode == SOLCLIENT_DELIVERY_MODE_PERSISTENT and publish_status == SOLCLIENT_WOULD_BLOCK \
                    and self._publisher_back_pressure_type == PublisherBackPressure.No:
                raise PublisherOverflowError(WOULD_BLOCK_EXCEPTION_MESSAGE)

            if publish_status == SOLCLIENT_WOULD_BLOCK and \
                    self._publisher_back_pressure_type != PublisherBackPressure.No:
                self._process_would_block_status()
            return publish_status
        except (PubSubPlusClientError, PublisherOverflowError) as exception:
            if self._publisher_back_pressure_type != PublisherBackPressure.No and \
                    self._delivery_mode == SOLCLIENT_DELIVERY_MODE_DIRECT:
                self.notify_publish_error(exception, publishable.get_message(), publishable.get_destination())
            else:
                if not self._messaging_service.is_connected:
                    self.adapter.warning(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED)
                    raise IllegalStateError(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED) from exception
                self.adapter.warning(exception)  # pragma: no cover # Due to core error scenarios
                raise exception  # pragma: no cover # Due to core error scenarios

    def message_publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                        additional_message_properties: typing.Dict[str, Union[str, int, bytearray]] = None,
                        correlation_tag=None):  # pylint: disable=too-many-branches
        #     Sends message to the given destination(Topic)
        # Args:
        #         destination: Topic endpoint
        #         message: message payload
        #         additional_message_properties :
        #         correlation_tag
        # Raises:
        #     IllegalStateError: When publisher is NOT_STARTED/TERMINATED/NOT_READY
        #     PublisherOverflowError: When buffer queue is full
        #     SolaceWouldBlockException: When publisher receive WOULD_BLOCK
        #     PubSubPlusClientError: When unable to send message
        _PublisherUtilities.validate_topic_type(destination=destination, logger=logger)
        if not self.is_ready():
            if self._message_publisher_state == _MessagePublisherState.NOT_STARTED:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED)
            elif self._message_publisher_state == _MessagePublisherState.TERMINATED:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED)
            elif self._message_publisher_state == _MessagePublisherState.TERMINATING:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING)
            elif self._message_publisher_state == _MessagePublisherState.NOT_READY:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY)
                raise PublisherOverflowError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY)

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] enabled', self._publisher_back_pressure_type)
        if not isinstance(message, (OutboundMessage, str, bytearray)):
            raise InvalidDataTypeError(f"{type(message)} is unsupported at the "
                                       f"moment to publish a message")

        # convert bytearray & string type messages to OutboundMessage
        if not isinstance(message, OutboundMessage):
            self._message = self._outbound_message_builder.build(message)
        else:
            self._message = message
        if correlation_tag:
            set_correlation_tag_ptr(self._message.solace_message.msg_p, correlation_tag)

        self._message.solace_message.set_delivery_mode(self._delivery_mode)
        self._publishable = Publishable.of(self._message.solace_message, destination)
        # only add additional properties to publishable message self._message should not be modified
        if additional_message_properties:
            add_message_properties(additional_message_properties, self._publishable.get_message())
        if correlation_tag:
            if correlation_tag.startswith(b'publish_await'):  # inform  the broker to send ack ASAP
                # when its comes to  messages published via publish await acknowledgement method
                self._publishable.get_message().set_ack_immediately(True)
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            self._start_message_publisher_thread()
            self._handle_back_pressure(self._publishable)
        else:
            self.do_publish(self._publishable)

    def terminate_now(self):
        if not self._is_publisher_available_for_terminate():
            return

        with self._terminate_now_lock:
            # Even after acquiring lock still we have to check the state, since state can be modified by other threads
            if not self._is_publisher_available_for_terminate():
                return

            self._message_publisher_state = _MessagePublisherState.TERMINATING
            self._asked_to_terminate = True  # flag to prevent the thread to sleep while terminating
            self._handle_events_on_terminate()
            self._cleanup()
            self._check_unpublished_messages()

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # print("called terminate", datetime.datetime.now(), self._message_publisher_buffer_queue.qsize(), self.d,
        #       flush=True, )
        _Util.validate_grace_period_min(grace_period=grace_period, logger=logger)
        if not self._is_publisher_available_for_terminate():
            return

        with self._terminate_lock:
            # Even after acquiring lock still we have to check the state, since state can be modified by other threads
            if not self._is_publisher_available_for_terminate():
                return

            self._message_publisher_state = _MessagePublisherState.TERMINATING
            self._asked_to_terminate = True  # flag to prevent the thread to sleep while terminating
            self._handle_events_on_terminate()
            grace_period_in_seconds = _Util.convert_ms_to_seconds(grace_period)
            remaining_time = self._wait_on_publisher_thread(timeout=grace_period_in_seconds)
            timeout = remaining_time if self._message_publisher_thread else grace_period_in_seconds
            self._wait_on_delivery_listener_thread(timeout)
            self._cleanup()
            self._check_unpublished_messages()

    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS) -> concurrent.futures.Future:
        # Terminate the PersistentMessageReceiver asynchronously (non-blocking).
        _Util.validate_grace_period_min(grace_period=grace_period, logger=logger)
        if self.__is_in_terminal_state():
            return self._terminate_future

        with self._terminate_async_lock:
            if self.__is_in_terminal_state():
                return self._terminate_future

            with ThreadPoolExecutor() as executor:
                self._terminate_future = executor.submit(self.terminate, grace_period)
                return self._terminate_future

    def is_running(self) -> bool:
        # Method to validate publisher state is running
        # Returns:
        #     bool: True, if message publisher state is running else False
        is_running = self._message_publisher_state in [_MessagePublisherState.STARTED,
                                                       _MessagePublisherState.READY]
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] is running?: %s', type(self).__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        # Method to validate publisher state is terminated
        # Returns:
        #     bool: True, if message publisher state is terminated else False
        is_terminated = self._message_publisher_state == _MessagePublisherState.TERMINATED
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] is terminated?: %s', type(self).__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        # Method to validate publisher state is terminating
        # Returns:
        #     bool: True, if message publisher state is terminating else False
        is_terminating = self._message_publisher_state == _MessagePublisherState.TERMINATING
        self.adapter.debug('[%s] is terminating?: %s', type(self).__name__, is_terminating)
        return is_terminating

    def publisher_thread(self):  # pylint: disable=missing-function-docstring
        # Method for returning the publisher thread instance
        return self._message_publisher_thread

    def publisher_readiness_thread(self):  # pylint: disable=missing-function-docstring
        # Method for returning the publisher readiness thread instance
        return self._publisher_readiness_listener_thread

    def publisher_buffer_queue(self):  # pylint: disable=missing-function-docstring
        # Method for returning the publisher buffer queue
        return self._message_publisher_buffer_queue

    def is_publisher_buffer_queue_full(self) -> bool:  # pylint: disable=missing-function-docstring
        # Method to validate publisher_buffer_queue is full
        # Returns:
        #     bool: True if buffer full else False
        is_buffer_full = self._message_publisher_buffer_queue.full()
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('Is %s buffer/queue FULL? %s', type(self).__name__, is_buffer_full)
        return is_buffer_full

    @property
    def message_publisher_buffer_queue(self):  # pylint: disable=missing-function-docstring
        # Returns the publisher buffer queue
        return self._message_publisher_buffer_queue

    @property
    def listener(self):  # pylint: disable=missing-function-docstring
        # Returns the listener instance
        return self._listener

    @property
    def would_block_received(self):  # pylint: disable=missing-function-docstring
        # Returns the flag if the would block is being received
        if self._would_block_received.is_set():
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('Is WOULD_BLOCK received?: %s', self._would_block_received.is_set())
        return self._would_block_received

    @would_block_received.setter
    def would_block_received(self, status: bool):  # pylint: disable=missing-function-docstring
        # setter for would block, if occurs
        if logger.isEnabledFor(logging.DEBUG):
            self.adapter.debug('Set WOULD_BLOCK received status: %s', status)
        self._would_block_received = status

    @property
    def is_publisher_readiness_listener_notification_sent(self):  # pylint: disable=missing-function-docstring
        # get publisher readiness listener notification sent status
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('Is publisher readiness notified? %s', self._is_notified)
        return self._is_notified

    @is_publisher_readiness_listener_notification_sent.setter
    def is_publisher_readiness_listener_notification_sent(self, sent_status: bool):
        # set publisher readiness listener notification sent status
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('Set publisher readiness notification sent status: %s', self._is_notified)
        self._is_notified = sent_status

    @property
    def message_publisher_state(self):
        return self._message_publisher_state

    def _cleanup(self):
        self._asked_to_terminate = True  # flag to prevent  the thread to sleep while terminating
        self._message_publisher_state = _MessagePublisherState.TERMINATED
        self._stop_publisher_thread()
        self._stop_publisher_readiness_listener_thread()
        self.adapter.info("%s", PUBLISHER_TERMINATED)

    def _start_message_publisher_thread(self):
        # Method to starting the message publisher thread
        if self._message_publisher_thread is None:
            self._message_publisher_thread = MessagePublisherThread(self, self._messaging_service)
            self._message_publisher_thread.daemon = False
            self._message_publisher_thread.start()

    def _handle_back_pressure(self, publishable: 'TopicPublishable'):
        # Method for handling the back pressure
        # Args:
        #   publishable(TopicPublishable) : publishable object
        # Raises:
        #     SolaceWouldBlockException: if WOULD-BLOCK received
        #     PublisherOverflowError: if buffer FULL
        try:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug("%s", "Enqueue message to buffer/queue")
            self.can_peek_buffer_event.set()  # let the publisher thread peek the buffer
            if self._publisher_back_pressure_type == PublisherBackPressure.Reject:
                self._message_publisher_buffer_queue.put((self, publishable), block=False)
            else:
                self._message_publisher_buffer_queue.put((self, publishable))
        except queue.Full:
            self._handle_queue_full()

    def _is_message_service_connected(self):
        # Method to check message_service connected or not
        # Returns:
        #     True if connected
        # Raises:
        #     IllegalStateError: if message_service not connected
        if not self._messaging_service.is_connected:
            self.adapter.warning(PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED)
            raise IllegalStateError(PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED)
        return True

    def _process_would_block_status(self):
        # Method to update message publisher state if WOULD_BLOCK received.
        # Reset can_send_received EVENT and SET would_block_received event
        if self._publisher_back_pressure_type == PublisherBackPressure.No:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('WOULD_BLOCK received. MessagingService status: %s',
                                   self._messaging_service.api.message_service_state.name)
        else:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug('WOULD_BLOCK received. Queue Size: %d. MessagingService status: %s',
                                   self._message_publisher_buffer_queue.qsize(),
                                   self._messaging_service.api.message_service_state.name)
        with self._would_block_lock:
            if not self.would_block_received.is_set():
                # print("gonna clear can send event", flush=True)
                self._messaging_service.api.can_send_received.clear()  # the moment we get WOULD_BLOCK, reset this
                self.would_block_received.set()  # the moment we get WOULD_BLOCK, SET this event,
                # to know WOULD_BLOCK occurred
            #         # if self._message_publisher_state == _MessagePublisherState.TERMINATING:
            #         #     print("after clearing can send", self._messaging_service.api.can_send_received.is_set(),
            #         #           flush=True, )
            #             print( "after setting clearing would block",
            #                    self.would_block_received.is_set(), flush=True, )

        if self._publisher_back_pressure_type == PublisherBackPressure.No:
            self._message_publisher_state = _MessagePublisherState.NOT_READY
            self.adapter.warning(WOULD_BLOCK_EXCEPTION_MESSAGE)
            raise PublisherOverflowError(WOULD_BLOCK_EXCEPTION_MESSAGE)
        if self.is_publisher_buffer_queue_full():
            self._message_publisher_state = _MessagePublisherState.NOT_READY

    def _handle_queue_full(self):  # this method will raise an exception if the queue is full
        current_size = self._message_publisher_buffer_queue.qsize()
        raise PublisherOverflowError(f'{QUEUE_FULL_EXCEPTION_MESSAGE} Size: {current_size}')

    def _stop_publisher_thread(self):
        # This method is to stop publisher thread
        if self._message_publisher_thread is not None:
            self._can_peek_buffer_event.set()
            self._messaging_service.api.can_send_received.set()
            self._publisher_thread_stop_event.set()
            self._message_publisher_thread.join()

    def _stop_publisher_readiness_listener_thread(self):
        # This method is to stop publisher readiness listener thread
        if self._publisher_readiness_listener_thread is not None:
            self._messaging_service.api.can_send_received.set()
            self._publisher_readiness_listener_thread_stop_event.set()
            self._publisher_readiness_listener_thread.join()

    def _is_publisher_available_for_terminate(self):
        if self._message_publisher_state == _MessagePublisherState.NOT_STARTED:
            self.adapter.debug('%s %s', PUBLISHER_UNAVAILABLE_FOR_TERMINATE,
                               self._message_publisher_state.name)
            return False
        elif self._is_already_terminated():
            return False
        return True

    def _is_already_terminated(self):
        # Return True if it is already TERMINATED
        if self._message_publisher_state == _MessagePublisherState.TERMINATED:
            self.adapter.debug(PUBLISHER_ALREADY_TERMINATED)
            return True
        return False

    def _check_unpublished_messages(self):
        if self._message_publisher_buffer_queue is not None and self._message_publisher_buffer_queue.qsize() != 0:
            message = f'{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER}. ' \
                      f'Unpublished message count: [{self._message_publisher_buffer_queue.qsize()}]'
            self.adapter.warning(message)
            self._message_publisher_buffer_queue = None
            raise IncompleteMessageDeliveryError(message)

    def _wait_on_publisher_thread(self, timeout) -> float:
        if self._message_publisher_thread:  # wait for the grace period only
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
            # for back pressure scenario
            self._publisher_empty.wait(timeout=timeout)  # first we are waiting for publisher
            # buffer to drain empty
            remaining_time = (end_time - datetime.datetime.now()).total_seconds()
            return 0 if remaining_time < 0 else remaining_time

    def _wait_on_delivery_listener_thread(self, timeout):
        # now we are waiting for ack buffer to drain empty with whatever
        # time remaining of grace_period if we have publisher thread
        # else whole grace period we will wait for delivery listener thread,
        if self._delivery_listener:
            self._delivery_receipt_empty.wait(timeout=timeout)

    def _handle_events_on_terminate(self):
        self._can_peek_buffer_event.set()  # wake up thread

    def __is_connecting(self):
        return self._start_future and self._message_publisher_state == _MessagePublisherState.STARTING

    def __is_connected(self):
        return self._start_future and self._message_publisher_state == _MessagePublisherState.STARTED

    def __is_in_terminal_state(self):
        return self._terminate_future and (self.__is_terminating() or self.__is_terminated())

    def __is_terminating(self):
        return self._terminate_future and self._message_publisher_state == _MessagePublisherState.TERMINATING

    def __is_terminated(self):
        return self._terminate_future and self._message_publisher_state == _MessagePublisherState.TERMINATED
