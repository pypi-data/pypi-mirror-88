# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

_USE_EXPERIMENTAL_APIS = False
def enable():
    """
    Enable usage of experimental APIs bundled with Couchbase.
    """
    global _USE_EXPERIMENTAL_APIS
    _USE_EXPERIMENTAL_APIS = True

def enabled_or_raise():
    if _USE_EXPERIMENTAL_APIS:
        return

    raise ImportError(
            "Your application has requested use of an unstable couchbase "
            "client API. Use "
            "couchbase_core.experimental.enable() to enable experimental APIs. "
            "Experimental APIs are subject to interface, behavior, and "
            "stability changes. Use at your own risk")
