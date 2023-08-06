# Author: Edielson P. Frigieri <edielsonpf@gmail.com>
#
# License: MIT

import pytest

from wsntk import network
from wsntk.network import NetworkLink

def test_base_link():
    # Test SensorNode creation with default values.
    
    sensor1 = SensorNode()
    sensor2 = SensorNode()

    link = NetworkLink((sensor1,sensor2))

    assert link.get_status() == 0

