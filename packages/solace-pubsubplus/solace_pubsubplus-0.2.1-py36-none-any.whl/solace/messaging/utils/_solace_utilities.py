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

# Module for solace internal utilities"
# pylint: disable=missing-module-docstring,too-many-arguments,inconsistent-return-statements,no-else-raise

import configparser
import os
from os.path import dirname

from solace.messaging._solace_logging._core_api_log import last_error_info
from solace.messaging.config._solace_message_constants import INVALID_DATATYPE, TOPIC_NAME_MAX_LENGTH, \
    TOPIC_NAME_TOO_LONG, VALUE_CANNOT_BE_NEGATIVE, GRACE_PERIOD_MIN_INVALID_ERROR_MESSAGE, GRACE_PERIOD_MIN_MS, \
    DICT_CONTAINS_NONE_VALUE, CCSMP_INFO_SUB_CODE, CCSMP_SUB_CODE, CCSMP_CALLER_DESC, CCSMP_INFO_CONTENTS, \
    CCSMP_RETURN_CODE
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    InvalidDataTypeError, IllegalArgumentError, IllegalStateError


class _Util:  # pylint: disable=missing-class-docstring,missing-function-docstring
    # Utilities class

    @staticmethod
    def is_type_matches(actual, expected_type, raise_exception=True, ignore_none=False, exception_message=None,
                        logger=None) -> bool:
        # Args:
        #     actual: target input parameter
        #     expected_type: compare ACTUAL data type with this
        #     raise_exception: if actual and expected date type doesn't matches
        #     ignore_none: ignore type check if ACTUAL is None
        #
        # Returns: True if actual and expected date type matches, else False
        if isinstance(actual, expected_type) or (ignore_none and actual is None):
            return True
        if raise_exception:
            if exception_message is None:
                exception_message = f'{INVALID_DATATYPE} Expected type: [{expected_type}], ' \
                                    f'but actual [{type(actual)}]'
            if logger is not None:
                logger.warning(exception_message)
            raise InvalidDataTypeError(exception_message)
        return False

    @staticmethod
    def read_solace_props_from_config(section):
        # Method to read the dictionary template based on the file path provided
        # Returns:
        #     dict template
        config_ini_file_name = 'config.ini'
        base_folder = dirname(dirname(dirname(__file__)))
        config_ini_full_path = os.path.join(base_folder, config_ini_file_name)

        try:
            config = configparser.ConfigParser()
            config.read(config_ini_full_path)
            config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
            if section not in config_parser_dict:
                raise PubSubPlusClientError(f'Unable to locate "{section}" properties in '
                                            f'[{config_ini_full_path}]')  # pragma: no cover
                # Ignored due to unexpected err scenario
            return config_parser_dict[section]
        except Exception as exception:  # pragma: no cover # Ignored due to unexpected err scenario
            raise PubSubPlusClientError(f'Unable to locate "{section}" properties in '
                                        f'[{config_ini_full_path}] Exception: {exception}') from exception

    @staticmethod
    def read_key_from_config(section: str, key_name: str):
        # Method to read the key name from the config.ini file

        # noinspection PyBroadException
        try:
            kvp = _Util.read_solace_props_from_config(section)
            return kvp[key_name]
        except PubSubPlusClientError:  # pragma: no cover # Ignored due to unexpected err scenario
            return None

    @staticmethod
    def get_last_error_info(return_code: int, caller_description: str, exception_message: str = None):
        last_error = last_error_info(return_code, caller_desc=caller_description)
        cleansed_last_error = f'Caller Description: {last_error[CCSMP_CALLER_DESC]}. ' \
                              f'Error Info Sub code: [{last_error[CCSMP_INFO_SUB_CODE]}]. ' \
                              f'Error: [{last_error[CCSMP_INFO_CONTENTS]}]. ' \
                              f'Sub code: [{last_error[CCSMP_SUB_CODE]}]. ' \
                              f'Return code: [{last_error[CCSMP_RETURN_CODE]}]'
        if exception_message:
            cleansed_last_error = f'{exception_message}\n{cleansed_last_error}'
        return cleansed_last_error

    @staticmethod
    def is_topic_valid(topic_name, logger, error_message):
        if topic_name is None or len(topic_name) == 0:
            logger.warning(error_message)
            raise IllegalArgumentError(error_message)
        if len(topic_name) > TOPIC_NAME_MAX_LENGTH:
            logger.warning(TOPIC_NAME_TOO_LONG)
            raise IllegalArgumentError(TOPIC_NAME_TOO_LONG)
        return True

    @staticmethod
    def is_not_negative(input_value, raise_exception=True, exception_message=None, logger=None) -> bool:
        _Util.is_type_matches(input_value, int, logger=logger)
        if input_value < 0:
            error_message = VALUE_CANNOT_BE_NEGATIVE if exception_message is None else exception_message
            if logger:
                logger.warning(error_message)
            if raise_exception:
                raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
        return False

    @staticmethod
    def convert_ms_to_seconds(milli_seconds):
        return milli_seconds / 1000

    @staticmethod
    def handle_none_for_str(input_value):
        if input_value is None:
            return str(None)
        return input_value

    @staticmethod
    def validate_grace_period_min(grace_period, logger):
        if grace_period < GRACE_PERIOD_MIN_MS:
            logger.warning(GRACE_PERIOD_MIN_INVALID_ERROR_MESSAGE)
            raise IllegalArgumentError(GRACE_PERIOD_MIN_INVALID_ERROR_MESSAGE)

    @staticmethod
    def raise_illegal_state_error(error_message, logger=None):
        if logger:
            logger.warning(error_message)
        raise IllegalStateError(error_message)

    @staticmethod
    def is_none_or_empty_exists(given_dict, error_message=None, logger=None, raise_error=True):
        is_none_exists = all((value == '' or value is None) for value in given_dict.values())
        if error_message is None:
            error_message = DICT_CONTAINS_NONE_VALUE
        if is_none_exists:
            if logger:
                logger.warning(error_message)
            if raise_error:
                raise IllegalArgumentError(error_message)
            else:
                return True
        return False
