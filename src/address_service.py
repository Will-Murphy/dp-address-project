import requests, configparser

from abc import ABC, abstractmethod

class AddressService (ABC): 
    """ 
    Abstract Class to standardize third party service specific implementation of the 
    dp-address-project specifications. 
    
    If a method is not provided by a particular service implmentation, the method should 
    raise an error and tell the user so e.g.:

    def reverse_geocode(self, params, data):
        raise NotImplementedError(f'{type(self).__name__} does not provide this service') 
    """

    @abstractmethod
    def load_config(self, config_file):
        """ Resonsible for loading configs and setting up client """
        pass

    
   
    @abstractmethod
    def send_request(self, params:dict,  data):
        """ Responsible for sending request to service and returning processed data """
        pass


    @abstractmethod
    def validate(self, params:dict, data ):
        """ 
        Reponsible for validating input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        pass 
    
    
    @abstractmethod
    def forward_geocode(self, params:dict, data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        pass 

    @abstractmethod
    def reverse_geocode(self, params:dict, data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        pass
    