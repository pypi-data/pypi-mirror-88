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
This module contains the abstract base class used to receive direct messages.

A DirectMessageReceiver can be instantiated to receive direct messages from a PubSub+ event broker.
"""
from abc import ABC
from ctypes import c_int, c_void_p, py_object, CFUNCTYPE

from solace.messaging.receiver.async_receiver_subscriptions import AsyncReceiverSubscriptions
from solace.messaging.receiver.message_receiver import MessageReceiver
from solace.messaging.receiver.receiver_subscriptions import ReceiverSubscriptions


class DirectMessageReceiver(MessageReceiver, ReceiverSubscriptions,
                            AsyncReceiverSubscriptions, ABC):
    """
    An abstract class that defines the interface to a PubSub+ direct message consumer/receiver.

    NOTE:
        A caller of any of blocking message receiving methods , those without the *async* suffix such as the
        :py:func:`solace.messaging.receiver.message_receiver.MessageReceiver.receive_message()` function.
        will receive a new message for each call.

    WARNING:
        When you use this class, these are some considerations to aware of:
            - Concurrent use of asynchronous and synchronous message receiving methods on a single instance of
              receiver can have some unintended side effects and should be avoided.
            - Asynchronous methods should NOT be called multiple times or in combination with blocking message
              receiving function on the same  :py:class:`solace.messaging.receiver.message_receiver.MessageReceiver`
              object to avoid any unintended side effects.

    """

    msg_callback_func_type = CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)
