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


"""
The `MessagingService` (:py:class:`solace.messaging.messaging_service`) is an abstract class that
represents the Solace PubSub+ messaging service.

The ``MessagingService`` is used to:

- connect the service
- disconnect the service
- create a ``MessagePublisherBuilder``
- create a ``MessageReceiverBuilder``


The builder for the `MessagingService contains` the configuration to identify:

- a Solace PubSub+ event broker
- the client to the Solace PubSub+ Event Broker
- messaging service characteristics such as flow control
"""

# pylint: disable= missing-function-docstring,protected-access

import concurrent
import ctypes
import datetime
import json
import logging
import threading
import uuid
import weakref
from abc import ABC, abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue

from solace.messaging import SolaceServiceAdapter
from solace.messaging._messaging_service_utility import get_transmitted_statistic, get_received_statistic, \
    reset_statistics, get_transmitted_statistics, get_received_statistics
from solace.messaging._solace_logging._core_api_log import set_log_file, set_core_api_log_level
from solace.messaging.builder._impl._direct_message_publisher_builder import _DirectMessagePublisherBuilder
from solace.messaging.builder._impl._direct_message_receiver_builder import _DirectMessageReceiverBuilder
from solace.messaging.builder._impl._persistent_message_publisher_builder import _PersistentMessagePublisherBuilder
from solace.messaging.builder._impl._persistent_message_receiver_builder import _PersistentMessageReceiverBuilder
from solace.messaging.builder.direct_message_publisher_builder import DirectMessagePublisherBuilder
from solace.messaging.builder.direct_message_receiver_builder import DirectMessageReceiverBuilder
from solace.messaging.builder.persistent_message_publisher_builder import PersistentMessagePublisherBuilder
from solace.messaging.builder.persistent_message_receiver_builder import PersistentMessageReceiverBuilder
from solace.messaging.config._ccsmp_property_mapping import mandatory_props
from solace.messaging.config._sol_constants import SOLCLIENT_SESSION_PROP_DEFAULT_COMPRESSION_LEVEL, \
    _SOLCLIENTSTATSRX, _SOLCLIENTSTATSTX, SOLCLIENT_SENT_STATS, SOLCLIENT_RECEIVED_STATS, SOLCLIENT_PROP_ENABLE_VAL, \
    SOLCLIENT_OK, SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE, MAX_RETRY_INTERVAL_MS
from solace.messaging.config._solace_message_constants import RECONNECTION_LISTENER_SHOULD_BE_TYPE_OF, \
    RECONNECTION_ATTEMPT_LISTENER_SHOULD_BE_TYPE_OF, STATS_ERROR, INTERRUPTION_LISTENER_SHOULD_BE_TYPE_OF, \
    UNSUPPORTED_METRIC_TYPE, ERROR_WHILE_RETRIEVING_METRIC, BROKER_MANDATORY_KEY_MISSING_ERROR_MESSAGE, \
    DISPATCH_FAILED, VALUE_OUT_OF_RANGE, UNABLE_TO_CONNECT_ALREADY_DISCONNECTED_SERVICE, \
    MESSAGE_SERVICE_CONNECTION_IN_PROGRESS, MESSAGE_SERVICE_DISCONNECT_ALREADY
from solace.messaging.config.authentication_strategy import AuthenticationStrategy, AuthenticationConfiguration
from solace.messaging.config.retry_strategy import RetryConfigurationProvider, RetryStrategy
from solace.messaging.config.solace_properties import client_properties
from solace.messaging.config.solace_properties.authentication_properties import SCHEME_BASIC_USER_NAME, \
    SCHEME_BASIC_PASSWORD, SCHEME, SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD, SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE, \
    SCHEME_SSL_CLIENT_CERT_FILE
from solace.messaging.config.solace_properties.service_properties import VPN_NAME, GENERATE_RECEIVE_TIMESTAMPS, \
    GENERATE_SEND_TIMESTAMPS
from solace.messaging.config.solace_properties.transport_layer_properties import HOST, RECONNECTION_ATTEMPTS, \
    RECONNECTION_ATTEMPTS_WAIT_INTERVAL, CONNECTION_ATTEMPTS_TIMEOUT, CONNECTION_RETRIES, COMPRESSION_LEVEL, \
    KEEP_ALIVE_INTERVAL
from solace.messaging.config.solace_properties.transport_layer_security_properties import TRUST_STORE_PATH, \
    CERT_VALIDATED, CERT_REJECT_EXPIRED, CERT_VALIDATE_SERVERNAME, TRUSTED_COMMON_NAME_LIST
from solace.messaging.config.transport_protocol_configuration import TransportProtocolConfiguration
from solace.messaging.config.transport_security_strategy import TransportSecurityStrategy
from solace.messaging.connections.async_connectable import AsyncConnectable
from solace.messaging.connections.connectable import Connectable
from solace.messaging.core import _solace_session
from solace.messaging.errors.pubsubplus_client_error import InvalidDataTypeError, IllegalArgumentError, \
    IllegalStateError
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.publisher._impl._outbound_message import _OutboundMessageBuilder
from solace.messaging.publisher.outbound_message import OutboundMessageBuilder
from solace.messaging.utils._solace_utilities import _Util
from solace.messaging.utils.error_monitoring import ErrorMonitoring
from solace.messaging.utils.manageable import Metric, ApiMetrics, Manageable

logger = logging.getLogger('solace.messaging.connections')

__all__ = ['MessagingServiceClientBuilder', 'ServiceEvent', 'MessagingService', 'ServiceInterruptionListener']


class ServiceEvent(ABC):
    """
    This class represents an event that can occur asynchronously on a
    :py:class:`solace.messaging.messaging_service.MessagingService` object.
    Applications that are interested in ``ServiceEvent`` objects must register a listener for the one of interest.
    The available listeners for service events are:
    * ``ReconnectionListener``:
    Handle ReconnectionListener (:py:class:`solace.messaging.messaging_service.ReconnectionListener`) service events.
    These events indicate that the service reconnected.
    * ``ReconnectionAttemptListener``:
    Handle ReconnectionAttemptListener (:py:class:`solace.messaging.messaging_service.ReconnectionAttemptListener`)
    events. These events indicate that the service is disconnected and reconnection has begun.
    """

    @abstractmethod
    def get_time_stamp(self) -> float:
        """
        Retrieves the timestamp of the event.

        Returns:
            float: The time the event occurred.
        """

    @abstractmethod
    def get_message(self) -> str:
        """
        Retrieves the message contents.

        Returns:
            str: An informational string that describes in further detail the cause of the event.
        """

    @abstractmethod
    def get_cause(self) -> 'PubSubPlusClientError':
        """
        Retrieves the cause of the client exception
        (:py:class:`solace.messaging.errors.pubsubplus_client_error.PubSubPlusClientError`).

        Returns:
            PubSubPlusClientError: The client error for the event.
        """

    @abstractmethod
    def get_broker_uri(self) -> str:
        """
        Retrieves the URI of the event broker.

        Returns:
            str: The event broker URI associated with the Messaging Service.
        """


class _ServiceEvent(ServiceEvent):  # pylint: disable=missing-class-docstring
    # implementation of service event abstract class

    def __init__(self, broker_uri: str, original_exception: PubSubPlusClientError, message: str,
                 time_stamp: float = datetime.datetime.utcnow()):
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('[%s] initialized', type(self).__name__)
        self.time_stamp = time_stamp
        self.broker_uri = broker_uri
        self.cause = original_exception
        self.message = message

    def get_time_stamp(self) -> float:
        # :returns: timestamp
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Get timestamp: [%f]', self.time_stamp)
        return self.time_stamp

    def get_message(self) -> str:
        #  :returns: message

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Get message: [%s]', self.message)
        return self.message

    def get_broker_uri(self) -> str:
        #  :returns: broker uri
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Get broker uri: [%s]', self.broker_uri)
        return self.broker_uri

    def get_cause(self) -> 'PubSubPlusClientError':
        #  Returns: cause

        if self.cause:
            cause = self.cause.args[0]
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('Get cause: [%s]', cause)
            return cause
        return None


class ReconnectionListener(ABC):  # pylint: disable=too-few-public-methods
    """A class interface definition for a ``ReconnectionListener``
    Applications interested in ``Reconnection`` events must instantiate
    an object implementing the ``ReconnectionListener`` class and register
    the listener with ``MessagingService.add_reconnection_listener()``.
    """

    @abstractmethod
    def on_reconnected(self, service_event: ServiceEvent):
        """
        Callback invoked by ``MessagingService`` (py:class:`solace.messaging.messaging_service.MessagingService`)
        object when it is successfully reconnected.

        Args:
            service_event (ServiceEvent):  The detailed information for the event.

        """


class ListenerThread(threading.Thread):  # pylint: disable=missing-class-docstring, missing-function-docstring
    # Thread used to dispatch received messages on a receiver.

    def __init__(self,
                 listener_queue: Queue, stop_event, can_listen_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_info = f"ListenerThread Id: {str(hex(id(self)))}"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        self.adapter.debug('THREAD: [%s] initialized', type(self).__name__)
        self._queue = listener_queue
        self._listener_thread_stop_event = stop_event
        self._can_listen_event = can_listen_event

    def run(self):
        # Start running thread
        self.adapter.debug('THREAD: [%s] started', type(self).__name__)
        while not self._listener_thread_stop_event.is_set():
            if not self._can_listen_event.is_set():
                self._can_listen_event.wait()
            if self._queue.qsize() > 0:
                event_handler, service_event = self._queue.get()
                if isinstance(service_event, _ServiceEvent):
                    try:
                        event_handler(service_event)
                    except Exception as exception:  # pylint: disable=broad-except
                        self.adapter.warning("%s %s", DISPATCH_FAILED, str(exception))


class ReconnectionAttemptListener(ABC):  # pylint: disable=too-few-public-methods
    """
       A class interface definition for a reconnection attempt event listener.
       Applications that are interested in ``ReconnectionAttempt`` events must instantiate
       an object implementing the ReconnectionAttemptListener class and register
       the listener with ``MessagingService.add_reconnection_attempt_listener``.
    """

    @abstractmethod
    def on_reconnecting(self, event: 'ServiceEvent'):
        """
        Callback executed for the ``MessagingService`` connection fails and reconnection attempts begin.

        Args:
            event (ServiceEvent): The Reconnection event with detailed information for each reconnection attempt.

        """


class ServiceInterruptionListener(ABC):  # pylint: disable=too-few-public-methods
    """An interface that abstracts notification about non recoverable service interruption."""

    @abstractmethod
    def on_service_interrupted(self, event: ServiceEvent):
        """Callback executed in situation when connection goes down and cannot be successfully restored.

        Args:
            event: The service interruption event describing nature of the failure.
        """


class MessagingService(Connectable, AsyncConnectable, Manageable, ErrorMonitoring, ABC):
    """
    This is an abstract class for the messaging service and inherits ``Connectable``, ``AsyncConnect``, ``Manageable``,
    and ``ErrorMonitoring``. It contains abstract methods for connecting, disconnecting a service in both blocking
    and non-blocking mode and also contains the factory methods to create builders for a
    message receiver (:py:class:`solace.messaging.builder.message_receiver_builder.MessageReceiverBuilder`)
    and message publishers (:py:class:`solace.messaging.builder.message_publisher_builder.MessagePublisherBuilder`).
    """

    @abstractmethod
    def create_direct_message_receiver_builder(self) -> DirectMessageReceiverBuilder:
        """
        Defines the interface for a builder to create direct message receiver.

        Returns:
            DirectMessageReceiverBuilder: An object that represents a direct message receiver.
        """

    @abstractmethod
    def create_direct_message_publisher_builder(self) -> DirectMessagePublisherBuilder:
        """
        Defines the interface for a builder to create a direct message publisher.

        Returns:
            DirectMessagePublisherBuilder: An object that represents a direct message publisher.
        """

    @abstractmethod
    def create_persistent_message_receiver_builder(self) -> PersistentMessageReceiverBuilder:
        """
        Defines the interface for a builder to create a persistent message receiver.

        Returns:
            PersistentMessageReceiverBuilder: An object that represents a persistent message receiver.

        """

    @abstractmethod
    def create_persistent_message_publisher_builder(self) -> PersistentMessagePublisherBuilder:
        """
        Defines the interface for a builder to create a persistent message publisher.

        Returns:
            PersistentMessagePublisherBuilder: An object that represents a persistent message publisher.
        """

    @abstractmethod
    def get_application_id(self):
        """
        Retrieves the application identifier.

        Returns:
           The application identifier.
        """

    @abstractmethod
    def message_builder(self) -> OutboundMessageBuilder:
        """
        Defines the interface for a builder to create an outbound message.

        Returns:
            OutboundMessageBuilder: An object that represents the outbound message.
        """

    @staticmethod
    def builder():
        """
        Retrieves a ``MessagingServiceClientBuilder`` object.

        Returns:
            MessagingServiceClientBuilder: A builder object for the message service.
        """
        return MessagingServiceClientBuilder()

    @staticmethod
    def set_core_messaging_log_level(level: str, file=None):
        """
        Sets the core (Native) API log level. The Native API only generates logs at the given level or higher,
        which may be further filtered by Python logging.

        WARNING:
            Don't set the message log level to be too high or you'll impact the
            messaging service performance. For example, though it may seem like a good idea
            to set the core log level to a **DEBUG** level and then rely on Python logging to filter the logs,
            doing so severely affects the  messaging service performance. For this reason, don't do this.
            The core log level must be set lower than **WARNING** as a diagnostic aid.

        Args:
            file(str): The name of the file.
            level(str): A valid string representation of the Python logging level you want using one of the
            following values (ordered from lowest to highest), CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.

        """
        set_log_file(file)
        set_core_api_log_level(level)


class _ApiMetrics(ApiMetrics):  # pylint: disable=missing-class-docstring
    def __init__(self, messaging_service):
        self._messaging_service = messaging_service

    def get_value(self, the_metric: Metric) -> int:
        # Returns the metrics current value/count
        try:
            if the_metric.value in _SOLCLIENTSTATSTX.__members__:
                return get_transmitted_statistic(self._messaging_service.session_pointer,
                                                 _SOLCLIENTSTATSTX[the_metric.value].value)
            if the_metric.value in _SOLCLIENTSTATSRX.__members__:
                return get_received_statistic(self._messaging_service.session_pointer,
                                              _SOLCLIENTSTATSRX[the_metric.value].value)
            return None
        except AttributeError as exception:
            logger.warning("%s Exception %s", UNSUPPORTED_METRIC_TYPE, exception)
            raise InvalidDataTypeError(f'{UNSUPPORTED_METRIC_TYPE} {exception}') from exception
        except Exception as exception:
            logger.warning("%s Exception %s", ERROR_WHILE_RETRIEVING_METRIC, exception)
            raise PubSubPlusClientError(f'{ERROR_WHILE_RETRIEVING_METRIC} {exception}') from exception

    def reset(self):
        # Resets ALL stats
        reset_statistics(self._messaging_service.session_pointer)

    @staticmethod
    def __get_stats(arr, stat_info, api_metric) -> dict:
        # Method for getting the statistics
        stats = dict()
        arr_list = list(arr)
        api_metrics_values = set(item.value for item in Metric)
        for metric_type, metric_value in enumerate(arr_list):
            stats[stat_info(metric_type).name] = metric_value
            if stat_info(metric_type).name in api_metrics_values:
                for data in Metric:
                    if data.value == stat_info(metric_type).name:
                        api_metric[data.name] = metric_value
                        break
        return stats

    def __get_all_stats(self):
        # Method to get all API metrics for both transmitted and received statistics.
        api_metrics = dict()
        transmitted_core_metrics_arr = (ctypes.c_int64 * _SOLCLIENTSTATSTX[SOLCLIENT_SENT_STATS].value)()
        received_core_metrics_arr = (ctypes.c_int64 * _SOLCLIENTSTATSRX[SOLCLIENT_RECEIVED_STATS].value)()

        transmitted_metrics_status = get_transmitted_statistics(
            self._messaging_service.session_pointer,
            transmitted_core_metrics_arr)

        if transmitted_metrics_status != SOLCLIENT_OK:
            logger.warning(STATS_ERROR)
            raise PubSubPlusClientError(STATS_ERROR)

        self.__get_stats(transmitted_core_metrics_arr, _SOLCLIENTSTATSTX, api_metrics)

        received_metrics_status = get_received_statistics(self._messaging_service.session_pointer,
                                                          received_core_metrics_arr)

        if received_metrics_status != SOLCLIENT_OK:
            last_error_info = _Util.get_last_error_info(return_code=received_metrics_status,
                                                        caller_description='ApiMetrics->get_all_stats',
                                                        exception_message=STATS_ERROR)
            logger.warning(last_error_info)
            raise PubSubPlusClientError(last_error_info)

        self.__get_stats(received_core_metrics_arr, _SOLCLIENTSTATSRX, api_metrics)

        return api_metrics

    def __str__(self) -> str:
        # List of all in the API collected metrics
        return_value = _Util.handle_none_for_str(input_value=json.dumps(self.__get_all_stats()))
        return return_value


def listener_thread_cleanup(can_listen, stop_event, listener_thread):  # pylint: disable=missing-function-docstring
    if listener_thread is not None:
        can_listen.set()
        stop_event.set()
        listener_thread.join()


class _BasicMessagingService(MessagingService):  # pylint: disable=too-many-public-methods
    # pylint: disable=missing-class-docstring,too-many-instance-attributes
    #  Class implements all the methods of the MessagingService class and also have implementation for the
    #  reconnection listener and reconnection attempt listener adding and removal
    GENERATED_APP_ID_PREFIX = 'app_'

    def __init__(self, **kwargs):
        #
        # Args:
        #    **config (dict): Configuration details for creating messaging service
        #    **application_id (string) : application id value string or none
        #
        self._application_id = kwargs.get('application_id') or self.generate_random_application_id()  # holds the app id
        self._id_info = f"[SERVICE: {str(hex(id(self)))}] - [APP ID: {str(self._application_id)}]"
        self.adapter = SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)
        self._config = kwargs.get('config')  # stores the configuration values
        self._api = _solace_session._SolaceApi(self)  # this holds the instance of the SolaceApi
        self._config[client_properties.NAME] = self._application_id
        self._api.create_session(self._config)  # create the session as part of Messaging Service build process
        self._listener = set()
        self.attempt_listener_queue = None
        self.service_interruption_listener_queue = None
        self._listener_stop_event = threading.Event()
        self._listener_event = threading.Event()
        self._service_listener_stop_event = threading.Event()
        self._service_interruption_listener_thread: ListenerThread = None
        self._listener_thread = None
        self._attempt_listener_thread = None
        self._connect_future = None
        self._disconnect_future = None
        self._connect_lock = threading.Lock()
        self._connect_async_lock = threading.Lock()
        self._disconnect_lock = threading.Lock()
        self._disconnect_async_lock = threading.Lock()
        self.__api_metrics = _ApiMetrics(self)
        self._finalizer = weakref.finalize(self, listener_thread_cleanup, self._api.connection_can_listen,
                                           self._listener_stop_event, self._listener_thread)

    @property
    def logger_id_info(self):
        return self._id_info

    @property
    def api(self):  # pylint: disable=missing-function-docstring
        # this is a property which returns the SolaceApi instance
        return self._api

    def generate_random_application_id(self):  # pylint: disable=missing-function-docstring
        #
        # Method to generate random application id using uuid.
        # Returns:
        #    str: The return value. random alphanumeric string.
        #
        app_id = self.GENERATED_APP_ID_PREFIX + str(uuid.uuid4())
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Application id: [%s]', app_id)
        return app_id

    def connect(self):  # pylint: disable=protected-access
        #
        # Method to establish connection with event broker.
        # Returns:
        #    object: returns MessagingService object.

        # Raise error if message_service is already DISCONNECTING/DISCONNECTED
        if self._api.message_service_state in [_solace_session._MessagingServiceState.DISCONNECTING,
                                               _solace_session._MessagingServiceState.DISCONNECTED]:
            error_message = f'{UNABLE_TO_CONNECT_ALREADY_DISCONNECTED_SERVICE}{self._api.message_service_state.name}'
            self.adapter.warning(error_message)
            raise IllegalStateError(error_message)

        with self._connect_lock:
            # Connect message_service only if it is in INIT(NOT_CONNECTED) state
            if self._api.message_service_state == _solace_session._MessagingServiceState.NOT_CONNECTED:
                connect_status = self._api._session_connect()
                if connect_status != SOLCLIENT_OK:
                    self.adapter.warning("Connection failed. Status code: %s", connect_status)
                    raise PubSubPlusClientError(message=f"Connection failed. Status code: {connect_status}")
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug('[%s] connected', connect_status)
                return connect_status

            # Return OK if message_service state other than INIT(NOT_CONNECTED),
            # meaning CONNECT method is already invoked
            self.adapter.info('%s %s', MESSAGE_SERVICE_CONNECTION_IN_PROGRESS,
                              self._api.messaging_service_state.name)
            return SOLCLIENT_OK

    def connect_async(self) -> concurrent.futures.Future:
        # See the base class :py:class:`solace.messaging.connections.async_connectable.AsyncConnectable`
        #
        if self.__is_connecting():
            return self._connect_future

        with self._connect_async_lock:
            # Even after acquiring lock still we have to check the state to avoid spinning up the executor
            if self.__is_connecting():
                return self._connect_future

            with ThreadPoolExecutor(max_workers=1) as executor:
                self._connect_future = executor.submit(self.connect)
                return self._connect_future

    def disconnect(self):  # pylint: disable=protected-access
        #
        # Method to disconnect message service connection from event broker and stop reconnection
        # listener threads

        # Block message_service disconnect if it is in DISCONNECTING state
        with self._disconnect_lock:
            # Return OK if it is already DISCONNECTED
            if self.__is_disconnected():
                self.adapter.info("%s", MESSAGE_SERVICE_DISCONNECT_ALREADY)
                return SOLCLIENT_OK

            # Process disconnect if it is not disconnected
            self.__stop_listener_thread()
            return self._api.service_cleanup()

    def disconnect_async(self) -> concurrent.futures.Future:
        #
        # Method to asynchronous disconnect message service connection from event broker.
        #
        if self.__is_disconnecting():
            return self._disconnect_future

        with self._disconnect_async_lock:
            if self.__is_disconnecting():
                return self._disconnect_future

            with ThreadPoolExecutor(max_workers=1) as executor:
                self._disconnect_future = executor.submit(self.disconnect)
                return self._disconnect_future

    # need to remove
    def disconnect_force(self):  # pylint: disable=missing-function-docstring
        #
        # Method to disconnect with event broker.
        # HIGH RISK: We should use this only for testing.
        # In ideal scenario, we won't FORCE DISCONNECT SESSION
        # Returns:
        # object: returns MessagingService object.
        #
        return self._api.session_force_disconnect()

    def create_direct_message_receiver_builder(self) -> DirectMessageReceiverBuilder:
        #
        # Method to create direct message receiver builder class instance
        # Returns:
        #    object: returns DirectMessageReceiverBuilder object.
        #
        return _DirectMessageReceiverBuilder(messaging_service=self)

    def create_direct_message_publisher_builder(self) -> DirectMessagePublisherBuilder:
        # Method to create direct message publisher builder class instance
        # Returns:
        #     object: returns DirectMessagePublisherBuilder object.
        return _DirectMessagePublisherBuilder(messaging_service=self)

    def create_persistent_message_publisher_builder(self) -> PersistentMessagePublisherBuilder:
        # method to create persistent message publisher builder Class
        # Returns:
        #     PersistentMessagePublisherBuilder instance
        return _PersistentMessagePublisherBuilder(messaging_service=self)

    def create_persistent_message_receiver_builder(self) -> PersistentMessageReceiverBuilder:
        # method to create persistent message receiver builder Class
        # Returns:
        #     PersistentMessageReceiverBuilder instance
        return _PersistentMessageReceiverBuilder(self)

    def message_builder(self) -> OutboundMessageBuilder:
        # Method to return an instance of OutboundMessageBuilder
        return _OutboundMessageBuilder()

    def get_application_id(self):
        # property to return the application id.
        # Returns:
        #     gives application id
        return self._application_id

    def metrics(self):
        # Method to get metrics of transmitted/received data
        return self.__api_metrics

    @property
    def is_connected(self) -> bool:
        # property to know whether we are connected to event broker or not.
        # Returns:
        #     object: returns MessagingService object.
        return self._api.is_session_connected

    @property
    def session_pointer(self):  # pylint: disable=missing-function-docstring
        # returns underlying session pointer
        return self._api.session_pointer

    def __handle_listener_thread(self):
        if not self._api.listener_queue:
            self._api.listener_queue = Queue()
        if not self._listener_thread:
            self._listener_thread = ListenerThread(self._api.listener_queue, self._listener_stop_event,
                                                   self._api.connection_can_listen)
            self._listener_thread.daemon = False
            self._listener_thread.start()

    def add_reconnection_attempt_listener(self, listener: ReconnectionAttemptListener):
        # Method for adding the reconnection attempt listener
        #
        # Args:
        #     listener: reconnection attempt notification listener
        if isinstance(listener, ReconnectionAttemptListener):
            self._api.attempt_listeners.add(listener.on_reconnecting)
            self.__handle_listener_thread()
            return self
        self.adapter.warning("%s[%s]", RECONNECTION_ATTEMPT_LISTENER_SHOULD_BE_TYPE_OF,
                             ReconnectionAttemptListener)
        raise PubSubPlusClientError(message=f"{RECONNECTION_ATTEMPT_LISTENER_SHOULD_BE_TYPE_OF}"
                                            f"[{ReconnectionAttemptListener}]")

    def add_reconnection_listener(self, listener: ReconnectionListener):
        # Args:
        #     listener (ReconnectionListener): listener event
        #     args:
        if isinstance(listener, ReconnectionListener):
            self._api.reconnection_listeners.add(listener.on_reconnected)
            self.__handle_listener_thread()
            return self
        self.adapter.warning("%s[%s]", RECONNECTION_LISTENER_SHOULD_BE_TYPE_OF, ReconnectionListener)
        raise PubSubPlusClientError(message=f"{RECONNECTION_LISTENER_SHOULD_BE_TYPE_OF}[{ReconnectionListener}]")

    def add_service_interruption_listener(self, listener: ServiceInterruptionListener):
        # Method for adding the service interruption listener
        #
        # Args:
        #     listener: listener for identifying service interruptions
        if isinstance(listener, ServiceInterruptionListener):
            self._api.service_interruption_listeners.add(listener.on_service_interrupted)
            self.__handle_listener_thread()
            return self
        self.adapter.warning("%s[%s]", INTERRUPTION_LISTENER_SHOULD_BE_TYPE_OF, ServiceInterruptionListener)
        raise PubSubPlusClientError(message=f"{INTERRUPTION_LISTENER_SHOULD_BE_TYPE_OF}"
                                            f"[{ServiceInterruptionListener}]")

    def remove_reconnection_listener(self, listener: 'ReconnectionListener'):
        # Remove the reconnection listener.
        # Args:
        #    listener (ReconnectionListener): reconnection attempt notification listener
        #
        self._api.reconnection_listeners.remove(listener.on_reconnected)
        return self

    def remove_reconnection_attempt_listener(self, listener: 'ReconnectionAttemptListener'):
        # method to remove the reconnection attempt listener
        # Args:
        #    listener (ReconnectionAttemptListener): reconnection attempt notification listener
        #
        self._api.attempt_listeners.remove(listener.on_reconnecting)
        return self

    def remove_service_interruption_listener(self, listener: ServiceInterruptionListener):
        # method to remove the service interruption listener
        #
        # Args:
        #     listener: instance of the service interruption listener
        self._api.service_interruption_listeners.remove(listener.on_service_interrupted)
        return self

    def __str__(self):
        return f"application_id : {self._application_id} connected : {self.is_connected}"

    def __stop_listener_thread(self):
        # method for stopping the listener thread
        if self._listener_thread is not None:
            self._api.reconnection_listeners.clear()
            self._api.attempt_listeners.clear()
            self._api.service_interruption_listeners.clear()
            self._api.connection_can_listen.set()
            self._listener_stop_event.set()
            self._listener_thread.join()
            self._listener_thread = None

    def __is_connecting(self):
        return self._connect_future and \
               self._api.message_service_state == _solace_session._MessagingServiceState.CONNECTING

    def __is_disconnecting(self):
        return self._disconnect_future and \
               self._api.message_service_state == _solace_session._MessagingServiceState.DISCONNECTING

    def __is_disconnected(self):
        return self._api.message_service_state == _solace_session._MessagingServiceState.DISCONNECTED


class MessagingServiceClientBuilder(TransportProtocolConfiguration, AuthenticationConfiguration):
    """
     Builder class for messaging service builder
    """

    def __init__(self):
        # MessagingServiceClient builder
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('[%s] initialized', type(self).__name__)
        self._application_id = None
        self._stored_config = dict()

    def from_properties(self, config: dict):
        """
        Passes a configuration dictionary for configuration information.

        Args:
             config(dict): Pass a configuration dictionary.

        Returns:
            MessagingServiceClientBuilder: An object for method chaining.
        """
        if config is not None:
            self.__check_mandatory_props(config)
            broker_props = {HOST: config[HOST], VPN_NAME: config[VPN_NAME],
                            SCHEME_BASIC_USER_NAME: config[SCHEME_BASIC_USER_NAME],
                            SCHEME_BASIC_PASSWORD: config[SCHEME_BASIC_PASSWORD]}
            self._stored_config = broker_props
            if GENERATE_RECEIVE_TIMESTAMPS in config.keys() \
                    and config[GENERATE_RECEIVE_TIMESTAMPS] == SOLCLIENT_PROP_ENABLE_VAL:
                self._stored_config[GENERATE_RECEIVE_TIMESTAMPS] = SOLCLIENT_PROP_ENABLE_VAL
            if GENERATE_SEND_TIMESTAMPS in config.keys() and \
                    config[GENERATE_SEND_TIMESTAMPS] == SOLCLIENT_PROP_ENABLE_VAL:
                self._stored_config[GENERATE_SEND_TIMESTAMPS] = SOLCLIENT_PROP_ENABLE_VAL
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] from properties. \nHost: [%s] VPN name: [%s]\nUsername: [%s]',
                             MessagingService.__name__, config[HOST], config[VPN_NAME], config[SCHEME_BASIC_USER_NAME])
            self.__add_authentication_strategy(config)
            self.__add_reconnection_retry_strategy(config)
            self.__add_connection_retry_strategy(config)
            self.__add_transport_security_strategy(config)
            self.__add_message_compression(config)
            self.__add_keep_alive_interval(config)
        return self

    def with_authentication_strategy(self, authentication_strategy: AuthenticationStrategy) \
            -> 'MessagingServiceClientBuilder':
        """
        Configures the ``MessageService`` instance with the authentication strategy.
        For more information, see the base class
        :py:class:`solace.messaging.config.authentication_strategy.AuthenticationConfiguration`.

        Args:
            authentication_strategy(AuthenticationStrategy): The authentication strategy.
        """
        _Util.is_type_matches(authentication_strategy, AuthenticationStrategy, ignore_none=True)
        if authentication_strategy is not None:
            auth_properties = authentication_strategy.authentication_configuration
            self._stored_config = {**self._stored_config, **auth_properties}
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] with authentication strategy', MessagingService.__name__)
        return self

    def with_reconnection_retry_strategy(self, strategy: RetryStrategy):
        """
        Configures the ``MessageService`` instance with the reconnection retry strategy.
        For more information, see the base class
        :py:class:`solace.messaging.config.transport_protocol_configuration.TransportProtocolConfiguration`.

        Args:
            strategy(RetryStrategy): The retry strategy.
        """
        _Util.is_type_matches(strategy, RetryStrategy, ignore_none=True, logger=logger)
        if strategy is not None:
            retry_properties = RetryConfigurationProvider.to_reconnection_configuration(strategy)
            self._stored_config = {**self._stored_config, **retry_properties}
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] with reconnection retry strategy', MessagingService.__name__)
        return self

    def with_connection_retry_strategy(self, strategy: RetryStrategy):
        """
        Configures the ``MessageService`` instance with the connection retry strategy.
        For more information, see the base class
        :py:class:`solace.messaging.config.retry_strategy.RetryStrategy`.

        Args:
            strategy(RetryStrategy): The retry strategy.
        """
        _Util.is_type_matches(strategy, RetryStrategy, ignore_none=True, logger=logger)
        if strategy is not None:
            retry_properties = RetryConfigurationProvider.to_connection_configuration(strategy)  # Re-visit prop
            self._stored_config = {**self._stored_config, **retry_properties}
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] with connection retry strategy', MessagingService.__name__)
        return self

    def with_transport_security_strategy(self, transport_layer_security_strategy: TransportSecurityStrategy):
        """
        Configures a message with Transport Layer Security configuration.
        For more information, see the base class
        :py:class:`solace.messaging.config.transport_protocol_configuration.TransportProtocolConfiguration`.

        Args:
            transport_layer_security_strategy(TransportSecurityStrategy): The transport security strategy.
        """
        _Util.is_type_matches(transport_layer_security_strategy, TransportSecurityStrategy, ignore_none=True,
                              logger=logger)
        if transport_layer_security_strategy is not None:
            tls_properties = transport_layer_security_strategy.security_configuration
            self._stored_config = {**self._stored_config, **tls_properties}
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] with TLS strategy', MessagingService.__name__)
        return self

    def with_message_compression(self, compression_factor: int = SOLCLIENT_SESSION_PROP_DEFAULT_COMPRESSION_LEVEL):
        """
        Configures the ``MessageService`` instance with so that messages are compressed with ZLIB
        before transmission and decompressed on receive.
        """
        _Util.is_type_matches(compression_factor, int, ignore_none=True, logger=logger)
        if compression_factor is not None:
            self._stored_config = {**self._stored_config,
                                   **{COMPRESSION_LEVEL: compression_factor}}
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug('[%s] with message compression', MessagingService.__name__)
        return self

    def build(self, application_id=None) -> MessagingService:
        """
        Builds a ``MessagingService`` instance.

        Returns:
            MessagingService: A builder object for the Messaging Service.
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Build [%s]', MessagingService.__name__)

        return _BasicMessagingService(config=self._stored_config, application_id=application_id)

    @staticmethod
    def __check_mandatory_props(config: dict):
        if not all(key in config for key in mandatory_props):
            missing_keys = ','.join(set(mandatory_props) - set(config.keys()))
            error_message = f"{BROKER_MANDATORY_KEY_MISSING_ERROR_MESSAGE} {missing_keys}"
            logger.warning(error_message)
            raise PubSubPlusClientError(error_message)

    def __add_authentication_strategy(self, config: dict):
        if SCHEME_SSL_CLIENT_CERT_FILE in config.keys():
            self._stored_config[SCHEME] = SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE
            if SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD in config.keys():
                self._stored_config[SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD] = \
                    config[SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD]
            if SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE in config.keys():
                self._stored_config[SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE] = config[SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE]
            else:
                self._stored_config[SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE] = config[SCHEME_SSL_CLIENT_CERT_FILE]
            self._stored_config[SCHEME_SSL_CLIENT_CERT_FILE] = config[SCHEME_SSL_CLIENT_CERT_FILE]

    def __add_reconnection_retry_strategy(self, config: dict):
        if RECONNECTION_ATTEMPTS in config.keys():
            _Util.is_type_matches(config[RECONNECTION_ATTEMPTS], int, logger=logger)
            self._stored_config[RECONNECTION_ATTEMPTS] = config[RECONNECTION_ATTEMPTS]
        if RECONNECTION_ATTEMPTS_WAIT_INTERVAL in config.keys():
            _Util.is_type_matches(config[RECONNECTION_ATTEMPTS_WAIT_INTERVAL], int)
            if config[RECONNECTION_ATTEMPTS_WAIT_INTERVAL] < 0 or \
                    config[RECONNECTION_ATTEMPTS_WAIT_INTERVAL] > MAX_RETRY_INTERVAL_MS:
                logger.warning("%s [0-%d]", VALUE_OUT_OF_RANGE, MAX_RETRY_INTERVAL_MS)
                raise IllegalArgumentError(f"{VALUE_OUT_OF_RANGE} [0-{MAX_RETRY_INTERVAL_MS}]")
            self._stored_config[RECONNECTION_ATTEMPTS_WAIT_INTERVAL] = config[RECONNECTION_ATTEMPTS_WAIT_INTERVAL]

    def __add_connection_retry_strategy(self, config: dict):
        if CONNECTION_RETRIES in config.keys():
            _Util.is_type_matches(config[CONNECTION_RETRIES], int, logger=logger)
            self._stored_config[CONNECTION_RETRIES] = config[CONNECTION_RETRIES]
        if CONNECTION_ATTEMPTS_TIMEOUT in config.keys():
            _Util.is_type_matches(config[CONNECTION_ATTEMPTS_TIMEOUT], int)
            if config[CONNECTION_ATTEMPTS_TIMEOUT] < 0 or \
                    config[CONNECTION_ATTEMPTS_TIMEOUT] > MAX_RETRY_INTERVAL_MS:
                logger.warning("%s [0-%d]", VALUE_OUT_OF_RANGE, MAX_RETRY_INTERVAL_MS)
                raise IllegalArgumentError(f"{VALUE_OUT_OF_RANGE} [0-{MAX_RETRY_INTERVAL_MS}]")
            self._stored_config[CONNECTION_ATTEMPTS_TIMEOUT] = config[CONNECTION_ATTEMPTS_TIMEOUT]

    def __add_transport_security_strategy(self, config: dict):
        if TRUST_STORE_PATH in config.keys():
            self._stored_config[TRUST_STORE_PATH] = config[TRUST_STORE_PATH]
        if CERT_VALIDATED in config.keys() and isinstance(config[CERT_VALIDATED], bool):
            self._stored_config[CERT_VALIDATED] = config[CERT_VALIDATED]
        if CERT_REJECT_EXPIRED in config.keys() and isinstance(config[CERT_REJECT_EXPIRED], bool):
            self._stored_config[CERT_REJECT_EXPIRED] = config[CERT_REJECT_EXPIRED]
        if CERT_VALIDATE_SERVERNAME in config.keys():
            self._stored_config[CERT_VALIDATE_SERVERNAME] = config[CERT_VALIDATE_SERVERNAME]
        if TRUSTED_COMMON_NAME_LIST in config.keys():
            self._stored_config[TRUSTED_COMMON_NAME_LIST] = config[TRUSTED_COMMON_NAME_LIST]

    def __add_message_compression(self, config: dict):
        if COMPRESSION_LEVEL in config.keys():
            _Util.is_type_matches(config[COMPRESSION_LEVEL], int, logger=logger)
            self._stored_config[COMPRESSION_LEVEL] = config[COMPRESSION_LEVEL]

    def __add_keep_alive_interval(self, config: dict):
        if KEEP_ALIVE_INTERVAL in config.keys():
            _Util.is_type_matches(config[KEEP_ALIVE_INTERVAL], int, logger=logger)
            self._stored_config[KEEP_ALIVE_INTERVAL] = config[KEEP_ALIVE_INTERVAL]
