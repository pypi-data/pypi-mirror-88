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


# Abstract base class for DirectMessageReceiverBuilder """  # pylint: disable=missing-module-docstring

from typing import List

from solace.messaging.builder.message_receiver_builder import MessageReceiverBuilder
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.utils._solace_utilities import _Util


class _MessageReceiverBuilder(MessageReceiverBuilder):
    def __init__(self, messaging_service: 'MessagingService'):
        self._messaging_service: 'MessagingService' = messaging_service
        self._topic_subscriptions = list()

    def with_subscriptions(self, subscriptions: List[TopicSubscription]) -> \
            'MessageReceiverBuilder':
        _Util.is_type_matches(subscriptions, List, raise_exception=True)
        self._topic_subscriptions = list()
        for topic in subscriptions:
            _Util.is_type_matches(topic, TopicSubscription, raise_exception=True)
            self._topic_subscriptions.append(topic.get_name())
        return self

    def from_properties(self, configuration: dict) -> 'MessageReceiverBuilder':
        return self
