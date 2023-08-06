# Authors: Edielson P. Frigieri <edielsonpf@gmail.com> (main author)
#
# License: MIT

"""Sensor nodes for wirelesss sensor networks simulation."""

from abc import ABCMeta, abstractmethod

RADIO_CONFIG = {"DEFAULT":          {"min_tx_power": -10.0, "max_tx_power": 10.0, "rx_sensitivity": -100.0},
                "ESP32-WROOM-32U":  {"min_tx_power": -12.0, "max_tx_power": 9.0, "rx_sensitivity": -97.0}}

class BaseRadio(metaclass=ABCMeta):
    """Class for sensor nodes."""
    def __init__(self, tx_power = 5.0, radio = "DEFAULT"):
        self._set_radio_config(radio)
        self.set_txpower(tx_power)
                 
    def _set_radio_config(self, radio_type):
        radio_params = self._get_radio_params(radio_type)
        for param in radio_params: 
            if param == "max_tx_power":
               self.max_tx_power = radio_params[param]
            elif param == "min_tx_power":
               self.min_tx_power = radio_params[param]
            elif param == "rx_sensitivity":
               self.rx_sensitivity = radio_params[param]
            else:
                raise ValueError("Radio parameter not expected: %s." %(param))
    
    def _get_radio_params(self, radio_type):
        radio_type = str(radio_type).upper()
        try:
            return RADIO_CONFIG[radio_type]
        except KeyError as e:
            raise ValueError("Radio %s is not supported." % radio_type) from e


    def set_txpower(self, tx_power):
        """Set radio transmission power
        Parameters
        ----------
        tx_power : {float}
            Transmission power to be configured in the radio
        
        Returns
        -------
        No data returned
        """
        
        if((tx_power >= self.min_tx_power) and (tx_power <= self.max_tx_power)):
            self.tx_power = tx_power    
        else:
            raise ValueError("Parameter out of radio power specification. Expected value from %s dBm to %s dBm." %(self.min_tx_power, self.max_tx_power))
                        

    def get_txpower(self):
        """Get radio transmission power
        Parameters
        ----------
        No parameters
        
        Returns
        -------
        float number
            The current configured transmission power
        """
        return self.tx_power

    def get_rxsensitivity(self):
        """Get radio receiver sensitivity
        Parameters
        ----------
        No parameters
        
        Returns
        -------
        float number
            The current configured receiver sensitivity
        """
        return self.rx_sensitivity


class SensorNode(BaseRadio):
    """Class for sensor nodes."""
    def __init__(self, position = (0.0, 0.0), tx_power = 5.0, radio = "DEFAULT"):
        self.position = position
        super(SensorNode, self).__init__(tx_power, radio)
        
    def set_position(self, position):
        self.position = position    
        
    def get_position(self):
        return self.position


