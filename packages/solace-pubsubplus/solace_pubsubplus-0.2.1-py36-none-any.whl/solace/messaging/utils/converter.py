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
This module is for type-safe object converter.
"""
from abc import ABC, abstractmethod
from typing import Union, TypeVar, Generic

T = TypeVar('T')  # pylint: disable=invalid-name


class BytesToObject(Generic[T], ABC):  # pylint: disable=too-few-public-methods
    """A class that converts  a ``bytearray`` object to a business object."""

    @abstractmethod
    def convert(self, src: bytearray) -> T:
        """
        Converts the ``bytearray`` to an business object.

        Args:
            src (bytearray): The byte array to convert to a business object.

        Returns:
            T: The converted business object.

        """


class ObjectToBytes(Generic[T], ABC):  # pylint: disable=too-few-public-methods
    """A class that converts business objects to a ``bytes`` arrays and ``bytearrays`` to business objects."""

    @abstractmethod
    def to_bytes(self, src: T) -> bytes:
        """
        Converts the provided business object into a ``bytearray`` value.

        Args:
            src(T): The business object to convert.

        Args:
            bytes: The bytes object from the converted business object.
        """

    @abstractmethod
    def get_message_properties(self) -> Union[dict, None]:
        """
        Provides optional message header properties that are included in an outbound message during message
        composition using provided instance of converter. The developer of the particular converters may
        decide to inject some message header properties as part of the business object conversion to a message
        (i.e., schema URL is a good candidate for this). This method is called from the API at appropriate time
        to retrieve the desired message properties and inject them into a message.

        Returns:
            dict: A dictionary of the message properities. The default implementation returns None
            (no additional properties will be added).

        """
