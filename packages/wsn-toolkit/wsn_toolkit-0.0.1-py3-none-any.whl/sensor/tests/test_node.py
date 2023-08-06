# Author: Edielson P. Frigieri <edielsonpf@gmail.com>
#
# License: MIT

import pytest

from wsntk import sensor
from wsntk.sensor import SensorNode

def test_sensor_node():
    # Test SensorNode creation with default values.
    
    sensor = SensorNode()
    assert sensor.get_txpower() == 5.0

def test_set_position():
    # Test setting the a new position.
    
    sensor = SensorNode()
    
    position = (0.5,0.5)
    sensor.set_position(position)

    assert sensor.get_position() == position

def test_sensor_node_with_unkown_radio_raises_value_error():
    # Test SensorNode creation with a unknown radio type.
    
    error_msg = ('Radio UNKNOWN is not supported.')
        
    with pytest.raises(ValueError, match=error_msg):
        sensor = SensorNode(radio = "UNKNOWN")

def test_sensor_node_wrong_tx_power_raises_value_error():
    # Test exception when instatiationg a sensor node with the tx_power above expected range.
    
    error_msg = ('Parameter out of radio power specification. Expected value from -12.0 dBm to 9.0 dBm.')
        
    with pytest.raises(ValueError, match=error_msg):
        sensor = SensorNode(tx_power = 10.0, radio = "ESP32-WROOM-32U")
    
def test_set_tx_power_within_range():
    # Test setting the tx_power within expected range.
    
    sensor = SensorNode(radio = "ESP32-WROOM-32U")
    sensor.set_txpower(8.0)
    assert sensor.get_txpower() == 8.0


def test_set_tx_power_below_range_raises_value_error():
    # Test exception when setting the tx_power below expected range.
        
    error_msg = ('Parameter out of radio power specification. Expected value from -12.0 dBm to 9.0 dBm.')
        
    sensor = SensorNode(radio = "ESP32-WROOM-32U")
    
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_txpower(-13.0)


def test_set_tx_power_above_range_raises_value_error():
    # Test exception when setting the tx_power above expected range.
    
    error_msg = ('Parameter out of radio power specification. Expected value from -12.0 dBm to 9.0 dBm.')
        
    sensor = SensorNode(radio = "ESP32-WROOM-32U")
    
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_txpower(10.0)

def test_get_rx_sensitivity():
    # Test getting the rx sensitivity.
    
    sensor = SensorNode(radio = "ESP32-WROOM-32U")
    assert sensor.get_rxsensitivity() == -97.00
    