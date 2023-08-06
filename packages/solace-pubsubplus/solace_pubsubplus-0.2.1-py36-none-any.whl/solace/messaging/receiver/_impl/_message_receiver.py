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
# pylint: disable=missing-function-docstring,no-else-raise,no-member

"""
Module that abstracts message receiving behavior; it is a base class for all receivers.
"""
import concurrent
import logging
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum
from queue import Queue

from solace.messaging import SolaceServiceAdapter
from solace.messaging.config._solace_message_constants import GRACE_PERIOD_MAX_MS, \
    RECEIVER_TERMINATED_UNABLE_TO_START, CANNOT_ADD_SUBSCRIPTION, RECEIVER_TERMINATED, \
    CANNOT_REMOVE_SUBSCRIPTION, RECEIVER_UNAVAILABLE_FOR_TERMINATE, RECEIVER_ALREADY_TERMINATED, \
    UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_RECEIVER, UNABLE_TO_RECEIVE_MESSAGE_MESSAGE_SERVICE_NOT_CONNECTED, \
    RECEIVER_NOT_STARTED, UNABLE_TO_RECEIVE_MESSAGE_RECEIVER_ALREADY_TERMINATED
from solace.messaging.errors.pubsubplus_client_error import IllegalStateError, IncompleteMessageDeliveryError
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.message_receiver import MessageReceiver
from solace.messaging.utils._solace_utilities import _Util

logger = logging.getLogger('solace.messaging.receiver')


class _MessageReceiverState(Enum):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # enum class for defining the message receiver state
    NOT_STARTED = 0
    STARTING = 1
    STARTED = 2
    TERMINATING = 3
    TERMINATED = 4


class _MessageReceiver(MessageReceiver):  # pylint: disable=too-many-instance-attributes

    def __init__(self, messaging_service: '_BasicMessagingService'):
        self._messaging_service: '_BasicMessagingService' = messaging_service
        self._id_info = f"{self._messaging_service.logger_id_info} - " \
                        f"[RECEIVER: {str(hex(id(self)))}]"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        self._message_receiver_state = _MessageReceiverState.NOT_STARTED
        self._asked_to_terminate = False
        self._message_receiver_queue = Queue()  # queue does not have max size
        self._start_future = None
        self._terminate_future = None
        self._start_lock = threading.Lock()
        self._start_async_lock = threading.Lock()
        self._terminate_now_lock = threading.Lock()
        self._terminate_lock = threading.Lock()
        self._terminate_async_lock = threading.Lock()
        self._id_info = f"[SERVICE: {str(hex(id(self._messaging_service)))}] [RECEIVER: {str(hex(id(self)))}]"
        self._receive_lock = threading.Lock()

    def is_running(self) -> bool:
        is_running = self._message_receiver_state == _MessageReceiverState.STARTED
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('%s is running?: %s', type(self).__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        is_terminated = _MessageReceiverState.TERMINATED == self._message_receiver_state
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('%s  is terminated?: %s', type(self).__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        is_terminating = _MessageReceiverState.TERMINATING == self._message_receiver_state
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('%s is terminating?', is_terminating)
        return is_terminating

    @property
    def asked_to_terminate(self):
        return self._asked_to_terminate

    def start(self):
        # Raise error if receiver is already TERMINATING/TERMINATED
        self._is_receiver_terminated(error_message=RECEIVER_TERMINATED_UNABLE_TO_START)

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

    def receive_async(self, message_handler: 'MessageHandler'):
        pass

    def receive_message(self, timeout=None) -> InboundMessage:
        pass

    def _check_buffer(self):
        if self._message_receiver_queue in self._messaging_service.api.receiver_queues:
            # by pop-ing out we make sure callback also don't insert extra None in buffer,
            # since flow down event is received  first before we receive SOLCLIENT_SESSION_EVENT_DOWN_ERROR
            index = self._messaging_service.api.receiver_queues.index(self._message_receiver_queue)
            self._messaging_service.api.receiver_queues.pop(index)

    def terminate_now(self):
        # implementation will be  given in direct & persistent concrete class
        if not self._is_receiver_available_for_terminate():
            return

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # implementation will be  given in direct & persistent concrete class
        _Util.validate_grace_period_min(grace_period=grace_period, logger=logger)
        if not self._is_receiver_available_for_terminate():
            return

    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS) -> concurrent.futures.Future:
        # Terminate the PersistentMessageReceiver asynchronously (non-blocking).
        _Util.validate_grace_period_min(grace_period=grace_period, logger=logger)
        if self.__is_in_terminal_state():
            return self._terminate_future

        with self._terminate_async_lock:
            # Even after acquiring lock still we have to check the state to avoid spinning up the executor
            if self.__is_in_terminal_state():
                return self._terminate_future

            with ThreadPoolExecutor() as executor:
                self._terminate_future = executor.submit(self.terminate, grace_period)
                return self._terminate_future

    def _can_add_subscription(self, error_message=None, raise_error=True):
        error_message = f'{CANNOT_ADD_SUBSCRIPTION}{self._message_receiver_state.name}' \
            if error_message is None else error_message
        self._is_receiver_available(error_message=error_message, raise_error=raise_error)

    def _can_remove_subscription(self, error_message=None, raise_error=True):
        error_message = f'{CANNOT_REMOVE_SUBSCRIPTION}{self._message_receiver_state.name}' \
            if error_message is None else error_message
        self._is_receiver_available(error_message=error_message, raise_error=raise_error)

    def _is_receiver_available(self, error_message=None, raise_error=True):
        self._is_receiver_started(error_message=error_message, raise_error=raise_error)
        self._is_receiver_terminated(error_message=error_message, raise_error=raise_error)

    def _is_receiver_available_for_terminate(self):
        self._is_receiver_started \
            (error_message=f'{RECEIVER_UNAVAILABLE_FOR_TERMINATE}{self._message_receiver_state.name}',
             raise_error=True)
        return not self._is_receiver_terminated(error_message=RECEIVER_ALREADY_TERMINATED, raise_error=False)

    def _is_receiver_started(self, error_message, raise_error=True):
        if self._message_receiver_state == _MessageReceiverState.NOT_STARTED:
            self.adapter.warning("%s", error_message)
            if raise_error:
                raise IllegalStateError(error_message)
            else:
                return False
        return True

    def _is_receiver_terminated(self, error_message=None, raise_error=True):
        if self._message_receiver_state == _MessageReceiverState.TERMINATED:
            error_message = RECEIVER_TERMINATED if error_message is None else error_message
            self.adapter.warning("%s", error_message)
            if raise_error:
                raise IllegalStateError(error_message)
            else:
                return True
        return False

    def _check_undelivered_messages(self):  # notify application of any remaining buffered data
        if self._message_receiver_queue is not None and self._message_receiver_queue.qsize() != 0:
            message = f'{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_RECEIVER}. ' \
                      f'Message count: [{self._message_receiver_queue.qsize()}]'
            self.adapter.warning("%s", message)
            self._message_receiver_queue = None
            raise IncompleteMessageDeliveryError(message)

    def _handle_events_on_terminate(self):
        # note this wakes the message delivery even when receiver is paused
        # this is better then blocking for the whole grace period
        self._can_receive_event.set()  # stop the thread from waiting

    def _is_message_service_connected(self, raise_error=True):
        # Method to validate message service is connected or not
        if not self._messaging_service.is_connected:
            self.adapter.warning("%s", UNABLE_TO_RECEIVE_MESSAGE_MESSAGE_SERVICE_NOT_CONNECTED)
            if raise_error:
                raise IllegalStateError(UNABLE_TO_RECEIVE_MESSAGE_MESSAGE_SERVICE_NOT_CONNECTED)
            else:
                return False
        return True

    def _is_started(self, raise_error=True):
        if self._message_receiver_state == _MessageReceiverState.NOT_STARTED:
            self.adapter.debug("%s", RECEIVER_NOT_STARTED)
            if raise_error:
                raise IllegalStateError(RECEIVER_NOT_STARTED)
            else:
                return False
        return True

    def _can_receive_message(self):
        # """can able to receive message if message service is connected and it is not terminating/terminated"""
        self._is_message_service_connected()
        self._is_receiver_terminated(error_message=UNABLE_TO_RECEIVE_MESSAGE_RECEIVER_ALREADY_TERMINATED)

    def __is_connecting(self):
        return self._start_future and self._message_receiver_state == _MessageReceiverState.STARTING

    def __is_connected(self):
        return self._start_future and self._message_receiver_state == _MessageReceiverState.STARTED

    def __is_in_terminal_state(self):
        return self._terminate_future and (self.__is_terminating() or self.__is_terminated())

    def __is_terminating(self):
        return self._terminate_future and self._message_receiver_state == _MessageReceiverState.TERMINATING

    def __is_terminated(self):
        return self._terminate_future and self._message_receiver_state == _MessageReceiverState.TERMINATED
