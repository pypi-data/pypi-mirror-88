# Copyright 2020 Josh Pieper, jjp@pobox.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

"""Classes and functions for interoperating with the moteus brushless
controller."""

__all__ = [
    'Fdcanusb', 'Router', 'Controller', 'Register', 'Transport',
    'PythonCan',
    'Mode', 'QueryResolution', 'PositionResolution', 'Command',
    'TRANSPORT_FACTORIES',
    'INT8', 'INT16', 'INT32', 'F32', 'IGNORE',
    'Pi3HatRouter',
]


from moteus.command import Command
from moteus.fdcanusb import Fdcanusb
from moteus.router import Router
from moteus.transport import Transport
from moteus.pythoncan import PythonCan
from moteus.moteus import (Controller, Register,
                           Mode, QueryResolution, PositionResolution,
                           TRANSPORT_FACTORIES)
from moteus.multiplex import (INT8, INT16, INT32, F32, IGNORE)


from moteus.pi3hat_router import Pi3HatRouter


class Pi3hatFactory():
    PRIORITY = 5

    def __call__(self):
        return Pi3HatRouter()


TRANSPORT_FACTORIES.append(Pi3hatFactory())

VERSION = "0.2.0"
