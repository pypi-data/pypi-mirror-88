# Authors: Edielson P. Frigieri <edielsonpf@gmail.com> (main author)
#
# License: MIT

"""Sensor networks simulation."""

from abc import ABCMeta, abstractmethod

LINK_STATUS_TYPE = {"inactive": 0, "active": 1}

class BaseLink(metaclass=ABCMeta):
    """Base class for network links between nodes."""
    def __init__(self, link = (SrcNode, DstNode), link_status = "inactive"):
        self.link = link
        self.link_status_type = _get_link_status_type(link_status)

    def set_status(self, link_status):
        self.status = _get_link_status_type(self, link_status)
        
    def get_status(self):
        return self.link_status_type
    
    def _get_link_status_type(self, link_status):
        link_status = str(link_status).lower()
        try:
            return LINK_STATUS[link_status]
        except KeyError as e:
            raise ValueError("Status %s is not supported." % link_status) from e


class NetworkLink(BaseLink):
    """Network links between sensor nodes."""
    
    def __init__(self, link = (SrcNode, DstNode), link_status = "inactive", link_cost = 0.0):
         super().__init__(link, link_status)
         self.link_cost = link_cost
         
    def set_link_cost(self, link_cost):
        """Set radio transmission power
        Parameters
        ----------
        tx_power : {float}
            Transmission power to be configured in the radio
        
        Returns
        -------
        No data returned
        """
        self.link_cost = link_cost    
                        

    def get_link_cost(self):
        """Get radio transmission power
        Parameters
        ----------
        No parameters
        
        Returns
        -------
        float number
            The current configured transmission power
        """
        return self.link_cost
