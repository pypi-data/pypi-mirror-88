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

# Module contains the publisher utility methods

# pylint: disable= missing-module-docstring, missing-class-docstring, missing-function-docstring,too-few-public-methods
# pylint: disable=protected-access

from solace.messaging.resources.topic import Topic
from solace.messaging.utils._solace_utilities import _Util


class _PublisherUtilities:
    # Publisher utilities

    @staticmethod
    def validate_topic_type(destination, logger=None):
        # To validate Topic type
        _Util.is_type_matches(destination, Topic, raise_exception=True, logger=logger)
