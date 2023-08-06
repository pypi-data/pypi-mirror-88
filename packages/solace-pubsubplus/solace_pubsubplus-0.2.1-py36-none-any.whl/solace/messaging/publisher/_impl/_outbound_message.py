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

# pylint: disable=unidiomatic-typecheck

"""Module contains the Implementation class and methods for the OutboundMessageBuilder and OutboundMessage"""

import ctypes
import logging
import weakref
from ctypes import c_char_p
from typing import TypeVar, Any, Dict, Union

from solace.messaging.config._sol_constants import SOLCLIENT_OK, SOLCLIENT_FAIL
from solace.messaging.config._solace_message_constants import INVALID_ADDITIONAL_PROPS, DICT_KEY_CANNOT_NONE
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.core.message import _Message
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, IllegalArgumentError
from solace.messaging.publisher._outbound_message_utility import container_add_byte_array, \
    container_add_string, container_add_int64, close_map, add_message_properties
from solace.messaging.publisher.outbound_message import OutboundMessageBuilder, OutboundMessage
from solace.messaging.utils._solace_utilities import _Util

logger = logging.getLogger('solace.messaging.publisher')


def map_cleanup(map_p):  # pylint: disable=missing-function-docstring
    if map_p:
        try:
            return_code = close_map(map_p)
            if return_code != SOLCLIENT_OK:
                last_error_info = _Util.get_last_error_info(return_code=return_code,
                                                            caller_description='outbound_message->map_cleanup',
                                                            exception_message='Failed to free up the map container')
                logger.warning(last_error_info)
        except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenarios
            logger.warning("Failed to free up the map container. Error: %s", str(exception))


class SolaceMap:  # pylint: disable=too-few-public-methods,missing-class-docstring, missing-function-docstring
    def __init__(self, solace_message=None, map_p=None):
        if map_p is not None:
            self._map_p = map_p
        else:
            self._map_p = ctypes.c_void_p()
            return_code = solace_message.message_create_user_property_map(map_p=self._map_p)
            if return_code != SOLCLIENT_OK:  # pragma: no cover # Ignored due to core error scenarios
                last_error_info = _Util.get_last_error_info(return_code=return_code,
                                                            caller_description='SolaceMap->init',
                                                            exception_message='Unable to set user property map')
                logger.warning(last_error_info)
                raise PubSubPlusClientError(last_error_info)
        self._finalizer = weakref.finalize(self, map_cleanup, self._map_p)

    @property
    def map_p(self):
        return self._map_p

    @staticmethod
    def get_map_from_message(solace_message):
        map_p = ctypes.c_void_p()
        return_code = solace_message.message_get_user_property_map(map_p)
        if return_code == SOLCLIENT_OK:
            return SolaceMap(None, map_p)
        return None

    @staticmethod
    def add_user_props_to_container(map_p, property_key: str, property_value: Any) \
            :  # pylint: disable=no-self-use
        #  Add user properties to the container
        # Args:
        #     property_key (str): key
        #     property_value (Any):  value
        #
        # Returns:

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Adding user property. Property key: [%s]. Property value: [%s]. '
                         'Type: [%s]', property_key, str(type(property_value)), property_value)
        if type(property_value) == int:  # for bool we have to rely on type instead of isinstance,
            # if we use isinstance for int we may accidentally handle bool too,
            # bool will be handled in future and this if condition also will be changed
            property_value = ctypes.c_int64(property_value)
            container_add_int64(map_p, property_value, property_key)
        elif isinstance(property_value, str):
            property_value = c_char_p(property_value.encode())
            container_add_string(map_p, property_value, property_key)
        elif isinstance(property_value, bytearray):
            char_array = ctypes.c_char * len(property_value)
            property_value = char_array.from_buffer(property_value)
            container_add_byte_array(map_p, property_value, ctypes.c_uint32(len(property_value)), property_key)
        else:
            logger.warning("The given property value type: %s is not supported", type(property_value))
            raise IllegalArgumentError(f"The given property value type : {type(property_value)} is not supported")


class _OutboundMessageBuilder(OutboundMessageBuilder) \
        :  # pylint: disable=missing-class-docstring, missing-function-docstring
    # This builder is used for building outbound messages which can hold any type of messages used for publish message

    T = TypeVar('T', bytearray, str, 'OutboundMessage')

    def __init__(self):
        # message pointer initialization & allocation takes place here
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('[%s] initialized', type(self).__name__)
        self._solace_message = _SolaceMessage()
        self.priority = None

    def from_properties(self, configuration: Dict[str, Union[str, int, bytearray]]) -> 'OutboundMessageBuilder':
        # This method takes dict and prepare message properties
        # Args:
        # configuration (Dict[str, Union[str, int, bytearray]]): The configuration dictionary, it can have the key
        #                                                        as string and the value can be either a string or
        #                                                        an integer or a bytearray.
        #
        # Returns:
        #
        add_message_properties(configuration, self._solace_message)
        return self

    def with_property(self, property_key: str, property_value: Union[str, int, bytearray]) -> 'OutboundMessageBuilder':
        #  create user property with the given key & value
        # Args:
        #     property_key (str): key
        #     property_value (str): value
        #
        # Returns:
        #     OutboundMessageBuilder
        # _Util.is_type_matches(property_key, str, logger=logger)
        # _Util.is_type_matches(property_key, Union[str, int, bytearray], logger=logger)
        if property_key in [None, '']:
            logger.warning(DICT_KEY_CANNOT_NONE)
            raise IllegalArgumentError(DICT_KEY_CANNOT_NONE)
        if property_value in [None, '']:
            logger.warning(INVALID_ADDITIONAL_PROPS)
            raise IllegalArgumentError(INVALID_ADDITIONAL_PROPS)
        add_message_properties({property_key: property_value}, self._solace_message)
        return self

    def with_expiration(self, timestamp: int) -> 'OutboundMessageBuilder':
        # set expiration time
        # Args:
        #     timestamp (int): timestamp in ms
        #
        # Returns:
        #     OutboundMessageBuilder
        _Util.is_type_matches(timestamp, int, logger=logger)
        _Util.is_not_negative(timestamp, logger=logger)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Set message expiration time: [%d]', timestamp)
        return_code = self._solace_message.set_message_expiration(timestamp)

        if return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util.get_last_error_info(return_code=return_code,
                                                    caller_description='OutboundMessageBuilder->with_expiration',
                                                    exception_message='Unable to set expiration time.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def with_priority(self, priority: int) -> 'OutboundMessageBuilder':
        # Set the priority (0 to 255), where zero is the lowest  priority
        # Args:
        #     priority (OutboundMessageBuilder.Priority): integer value
        #
        # Returns:
        #     OutboundMessageBuilder
        _Util.is_type_matches(priority, int, logger=logger)
        _Util.is_not_negative(priority, logger=logger)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('Set message priority: [%d]', priority)
        return_code = self._solace_message.set_message_priority(priority)

        if return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util.get_last_error_info(return_code=return_code,
                                                    caller_description='OutboundMessageBuilder->with_priority',
                                                    exception_message='Unable to set priority.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def with_sequence_number(self, sequence_number: int) -> 'OutboundMessageBuilder':
        # Set the sequence number for the message
        # Args:
        #     sequence_number (int):  Expecting a integer value
        #
        # Returns:
        #     OutboundMessageBuilder
        _Util.is_type_matches(sequence_number, int, logger=logger)
        _Util.is_not_negative(sequence_number, logger=logger)
        return_code = self._solace_message.set_message_sequence_number(sequence_number)

        if return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util \
            .get_last_error_info(return_code=return_code,
                                 caller_description='OutboundMessageBuilder->with_sequence_number',
                                 exception_message='Unable to set sequence number.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def with_application_message_id(self, application_message_id: str) -> 'OutboundMessageBuilder':
        # Set the application message id for a message from a str, or None to delete
        # Args:
        #     application_message_id (str):  application message id
        #
        # Returns:
        #     OutboundMessageBuilder
        _Util.is_type_matches(application_message_id, str, logger=logger)
        return_code = self._solace_message.set_message_application_message_id(application_message_id) \
            if application_message_id is not None else self._solace_message.delete_message_application_message_id()

        if return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util \
            .get_last_error_info(return_code=return_code,
                                 caller_description='_DirectMessageReceiver->with_application_message_id',
                                 exception_message='Unable to set application message id')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def with_application_message_type(self, application_message_type: str) -> 'OutboundMessageBuilder':
        # Set the application message type for a message from a string or None to delete
        # Args:
        #     application_message_type (str): application message type
        #
        # Returns:
        #     OutboundMessageBuilder
        _Util.is_type_matches(application_message_type, str, logger=logger)
        return_code = self._solace_message.set_message_application_message_type(application_message_type) \
            if application_message_type is not None else self._solace_message.delete_message_application_message_type()

        if return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util \
            .get_last_error_info(return_code=return_code,
                                 caller_description='_DirectMessageReceiver->with_application_message_type',
                                 exception_message='Unable to set application message type.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def with_http_content_header(self, content_type: str, content_encoding: str) -> 'OutboundMessageBuilder':
        # Setting the HTTP content type and encoding for a message from a string
        # Args:
        #     content_type (str):  expecting a valid content type
        #     content_encoding (str):  expecting a valid content  encoding
        # Returns:
        _Util.is_type_matches(content_type, str, logger=logger)
        _Util.is_type_matches(content_encoding, str, logger=logger)
        content_type_return_code = self._solace_message.set_message_http_content_type(content_type)
        if content_type_return_code != SOLCLIENT_OK:
            last_error_info = _Util \
                .get_last_error_info(return_code=content_type_return_code,
                                     caller_description='_DirectMessageReceiver->with_http_content_header',
                                     exception_message='Unable to set HTTP content type.')
            logger.warning(last_error_info)
            raise PubSubPlusClientError(last_error_info)

        content_encoding_return_code = self._solace_message.set_message_http_content_encoding(content_encoding)
        if content_encoding_return_code == SOLCLIENT_OK:
            return self
        last_error_info = _Util \
            .get_last_error_info(return_code=content_encoding_return_code,
                                 caller_description='_DirectMessageReceiver->with_http_content_header',
                                 exception_message='Unable to set HTTP content header.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)

    def build(self, payload: T, additional_message_properties: Dict[str, Union[str, int, bytearray]] = None,
              converter=None) -> '_OutboundMessage':
        # Args:
        #     payload (T): payload
        # Kwargs:
        #     additional_message_properties (Any): properties
        #     converter (Any): converter
        # Returns:

        # Here self.msg_p is a template for all the message's properties
        msg_p_dup = self._solace_message.message_duplicate()
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('BUILD [%s]', OutboundMessage.__name__)
        return_code = SOLCLIENT_FAIL
        if not converter:
            if isinstance(payload, bytearray):
                char_array = ctypes.c_char * len(payload)
                message = char_array.from_buffer(payload)
                return_code = msg_p_dup.message_set_binary_attachment(message)

            elif isinstance(payload, str):
                return_code = msg_p_dup.message_set_binary_attachment_string(payload)

            if additional_message_properties:
                _Util.is_none_or_empty_exists(additional_message_properties,
                                              error_message=INVALID_ADDITIONAL_PROPS, logger=logger)
                add_message_properties(additional_message_properties, msg_p_dup)
        elif converter:
            additional_properties = converter.get_message_properties()

            if additional_properties:
                add_message_properties(additional_properties, msg_p_dup)
            payload_bytes = converter.to_bytes(payload)
            char_array = ctypes.c_char * len(payload_bytes)
            message = char_array.from_buffer_copy(payload_bytes)
            return_code = msg_p_dup.message_set_binary_attachment(msg=message, msg_length=len(payload_bytes))

        if return_code == SOLCLIENT_OK:
            return _OutboundMessage(msg_p_dup)
        last_error_info = _Util \
            .get_last_error_info(return_code=return_code,
                                 caller_description='OutboundMessageBuilder->build',
                                 exception_message='Failed to create attachment for the message.')
        logger.warning(last_error_info)
        raise PubSubPlusClientError(last_error_info)


class _OutboundMessage(_Message, OutboundMessage):  # pylint: disable=missing-class-docstring
    # Implementation class for OutboundMessage abstract class

    def __init__(self, msg_p):
        # Args: msg_p:  SolaceMessage used to publish the message
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('[%s] initialized', type(self).__name__)
        super().__init__(msg_p)

    def __str__(self):
        return _Util.handle_none_for_str(input_value=self._solace_message.get_message_dump())
