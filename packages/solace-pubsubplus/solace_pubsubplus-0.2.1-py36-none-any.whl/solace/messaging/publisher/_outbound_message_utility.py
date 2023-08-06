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


# module contains the class and functions which actually make the call to ccsmp #pylint:disable=missing-module-docstring
# this is an internal utility module, used by implementors of the API.
# pylint: disable=missing-function-docstring,import-outside-toplevel

import ctypes
import logging
from ctypes import c_uint32, c_char_p, byref

import solace
from solace.messaging.config._solace_message_constants import INVALID_ADDITIONAL_PROPS, DICT_KEY_CANNOT_NONE
from solace.messaging.errors.pubsubplus_client_error import IllegalArgumentError

logger = logging.getLogger('solace.messaging.core.api')


def close_map(container_p):
    # Finish a map or stream. This action makes the opaque container pointer invalid and fixes the
    # structured data in memory.
    # Args:
    #   container_p : A pointer to the opaque container pointer. The pointer is
    #                        reset to NULL on return
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure.
    return solace.CORE_LIB.solClient_container_closeMapStream(byref(container_p))


def container_delete_field(container_p, name):
    # Remove a field from a map. This function returns an error if called on
    # a stream. The serialized map is scanned and the named field is removed.
    # All subsequent fields in the serialized map are moved; this can be a slow
    # operation.
    # Args:
    #   container_p : An opaque container pointer.
    #   name : The name of the field to remove.
    return solace.CORE_LIB.solClient_container_deleteField(container_p,
                                                           c_char_p(name.encode()))


def container_add_uint64(container_p, value, name):
    #   Add a unsigned signed 64-bit value to a map or stream. If the container is a stream, the
    #    name parameter must be NULL. If the container is a map, the name parameter
    #    must be non-NULL.
    # Args:
    #   container_p : An opaque container pointer.
    #   value : A  unsigned 64-bit value.
    #   name : The name of a field for a map. This parameter must be NULL for a stream.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure.
    #
    solace.CORE_LIB.solClient_container_addUInt64(container_p, value,
                                                  c_char_p(name.encode()))


def container_add_int64(container_p, value, name):
    #   Add a signed 64-bit value to a map or stream. If the container is a stream, the
    #    name parameter must be NULL. If the container is a map, the name parameter
    #    must be non-NULL.
    # Args:
    #   container_p : An opaque container pointer.
    #   value : A signed 64-bit integer value.
    #   name : The name of a field for a map. This parameter must be NULL for a stream.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure.
    #
    solace.CORE_LIB.solClient_container_addInt64(container_p, value,
                                                 c_char_p(name.encode()))


def container_add_string(container_p, value, name):
    # Add a null terminated string (ASCII or UTF-8) to a map or stream. If the container is a stream, the
    #    name parameter must be NULL. If the container is a map, the name parameter
    #    must be non-NULL
    # Args:
    #   container_p : An opaque container pointer.
    #   value :  A pointer to a NULL-terminated string.
    #   name : The name of a field for a map. This parameter must be NULL for a stream.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure.
    solace.CORE_LIB.solClient_container_addString(container_p, value,
                                                  c_char_p(name.encode()))


def container_add_byte_array(container_p, arr_p, length, name):
    # Add a byte array to a map or stream. If the container is a stream, the
    #    name parameter must be NULL. If the container is a map, the name parameter
    #    must be non-NULL.
    # Args:
    #   container_p : An opaque container pointer.
    #   value :  A pointer to a NULL-terminated string.
    #   name : The name of a field for a map. This parameter must be NULL for a stream.
    #   length :      The length of the byte array.
    #   name   :      The name of a field for a map. This parameter must be NULL for a stream.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure.
    solace.CORE_LIB.solClient_container_addByteArray(container_p, arr_p, length, c_char_p(name.encode()))


def get_next_field(container_p, field_p, name_p):
    #  Read the next field of the map (or stream, although this function is not preferred for streams).
    #
    #   For a map, this returns the next field in the map, including the name of
    #   the field. This allows the application to iterate over the contents of the
    #   map.
    #
    #   While this function will work for a stream, it is preferable to use
    #   solClient_container_getField or solClient_container_getXXX for a specific
    #   field type. If this routine is used, a NULL pointer is returned for the
    #   field name if the provided pointer to the field name is not NULL.
    #
    #   If the returned field is a container (map or stream), the container should
    #   later be closed by a call to SolClient_container_closeMapStream(). However, if it is not,
    #   the container is automatically closed when the associated message is freed through a call to
    #   SolClient_msg_free(), or if the parent container is closed.
    #   If the container is closed automatically, the application may not continue
    #   to use the container. Attempting to use a closed container
    #   will return an invalid pointer error (SOLCLIENT_SUBCODE_PARAM_NULL_PTR).
    # Args:
    #   container_p : An opaque container pointer.
    #   field_p :  The address of solClient_field_t where the API will return
    #                        field type and value.
    #   field_size :    sizeof(solClient_field_t). This parameter is used for backwards binary
    #                        compatibility if solClient_field_t grows.
    #   name_p       The address of the pointer where API will return a pointer to
    #                          the NULL-terminated field name. For a stream, the
    #                          passed in pointer can be NULL, and if not, the returned
    #                          pointer will be NULL.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL on failure. SOLCLIENT_EOS at end of container.
    return solace.CORE_LIB.solClient_container_getNextField(container_p, ctypes.byref(field_p),
                                                            ctypes.sizeof(field_p),
                                                            ctypes.byref(name_p))


def set_correlation_tag_ptr(msg_p, correlation_tag):
    #     Given a msg_p, set the Correlation Tag to the given pointer. The Correlation Tag is a
    #     local reference used by applications generating Guaranteed messages. Messages that are
    #     sent in either PERSISTENT or non-PERSISTENT mode can set the Correlation Tag,
    #     which is returned when the SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT event
    #     is later received. The solClient_session_eventCallbackInfo structured returned with the
    #     event contains a (void *) correlation_p which will be the same pointer the application
    #     initializes with this method.
    #     Important: <b>The Correlation Tag is not included in the
    #     transmitted message and is only used with the local API</b>.
    #
    #     This function is provided for high-performance applications that
    #     must be aware that the data referenced cannot be modified until the send
    #     operation completes.
    return solace.CORE_LIB.solClient_msg_setCorrelationTagPtr(msg_p,
                                                              ctypes.c_char_p(correlation_tag),
                                                              c_uint32(8))  # size is ignored


def add_message_properties(configuration, solace_message):
    from solace.messaging.publisher._impl._outbound_message import SolaceMap

    user_props = set(list(configuration.keys())) - set(
        list(solace_message.message_properties_mapping.keys()))
    # set the solace defined message properties
    solace_message.handle_message_properties(configuration)
    solace_map_dup = SolaceMap.get_map_from_message(solace_message)
    if solace_map_dup is None:
        solace_map_dup = SolaceMap(solace_message)
    for key, value in configuration.items():
        # only add user defined props skip the  properties defined by Solace
        if key in [None, '']:
            logger.warning(DICT_KEY_CANNOT_NONE)
            raise IllegalArgumentError(DICT_KEY_CANNOT_NONE)
        if value in [None, '']:
            logger.warning(INVALID_ADDITIONAL_PROPS)
            raise IllegalArgumentError(INVALID_ADDITIONAL_PROPS)
        if key in user_props:
            # remove any existing field
            container_delete_field(solace_map_dup.map_p, key)
            # add field value
            SolaceMap.add_user_props_to_container(solace_map_dup.map_p, key, value)
