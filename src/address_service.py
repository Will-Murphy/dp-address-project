import requests, configparser
from abc import ABC, abstractmethod

class AddressService (ABC): 
    ''' 
    Abstract Class outlining basic specifications for service specific implementation of the 
    dp-address-project. If a method is not provided by a particular service implmentation, the 
    method should raise an error and tell the user so. 
    '''

    # Resonsible for loading configs and setting up client 
    @abstractmethod
    def load_config(self, config_file):
        pass

    
    # Responsible for sending request to service and returning processed data
    @abstractmethod
    def send_request(self, params: dict):
        pass


    # reponsible for creating output address validation csv from processed adress 
    # data and writing it to precreated csv out file with (headers already done)
    @abstractmethod
    def validate(self, params:dict, data:str ):
        pass 
    
    
    # reponsible for creating output address geocoding csv from processed address 
    # data and writing it to precreated csv out file with (headers already done)
    @abstractmethod
    def geocode(self,params):
        pass 
    
    # responsible for combination of functionality of geocode and validate
    @abstractmethod
    def validate_and_geocode(self, params): 
        pass
