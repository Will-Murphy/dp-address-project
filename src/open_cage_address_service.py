import configparser

from address_service import AddressService
from address import Address

from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

class OpenCageAddressService (AddressService): 

    # TODO: add number of processed addresses variable 
    def __init__(self):
        self.client = None 


    def load_config(self, config_file):
        """ Resonsible for loading configs and setting up client """
        config = configparser.ConfigParser()
        config.read(config_file)
        auth_key = config.get('OPEN CAGE', 'key' )
        self.client = OpenCageGeocode(auth_key)

    
   
    def send_request(self, params,  address_data):
        """ Responsible for sending request to service and returning processed data """
       
        # forward geocoding 
        if int(params["options"]) == 1: 
            address_query = u'{address_data.input_string}'
            try:
                results = self.client.geocode(address_query)
                return results
            except RateLimitExceededError as rate_err:
                print(rate_err)
            except InvalidInputError as invalid_err:
                print(invalid_err)
                raise

        # reverse geocoding 
        elif int(params["options"]) == 3:
            latitude = address_data.latitude
            longitude = address_data.longitude
            print(latitude)
            print(longitude)
            try:
                results = self.client.reverse_geocode(latitude, longitude, language = 'de', no_annotations='1')
                return results
            except RateLimitExceededError as rate_err:
                print(rate_err)
            except InvalidInputError as invalid_err:
                print(invalid_err)
                raise




    def validate(self, params, data ):
        """ 
        Reponsible for validating input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        raise NotImplementedError(f'{type(self).__name__} does not provide this service')
        
    
    
    def forward_geocode(self, params, address_input_data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        processed_address_list = []
        for address in address_input_data: 
            result = self.send_request(params, address)
            if result and len(result):
                address.latitude = result[0]['geometry']['lat']
                address.longitude = result[0]['geometry']['lng']
            processed_address_list.append(address)
        return processed_address_list
        
        

            



    def reverse_geocode(self, params, address_input_data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a single Address object or Address object list depending on stream or batch input.
        """
        print(address_input_data[0].latitude)
        print(address_input_data[0].longitude)
        processed_address_list = []
        for address in address_input_data: 
            result = self.send_request(params, address)
            if result and len(result):
                address.line_1 = result[0]['formatted']
            processed_address_list.append(address)
        return processed_address_list
        
     