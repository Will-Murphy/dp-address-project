import configparser

from address_service import AddressService
from address import Address

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

class SmartyAddressService (AddressService):
    '''
    Class represents smarty Streets US_STREETS_API Specific implementation of AddressService class. 
    It implements that abstract class with some helper methods. 
    '''

    MAX_ADDRESSES_PER_REQUEST = 100 

    def __init__(self):
        self.client = None 

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        auth_id = config.get('SMARTY STREETS', 'id' )
        auth_token = config.get('SMARTY STREETS', 'key')
        api_credentials = StaticCredentials(auth_id, auth_token)
        self.client = ClientBuilder(api_credentials).build_us_street_api_client()

    #TODO: clarify naming in this function, add parameters for stream
    def send_request(self, params, data):
        try:
            self.client.send_batch(data)
            return data
        except exceptions.SmartyException as err:
            print(err)
            return
    
    #TODO: clarify naming in this function, add parameters for stream
    def prepare_smarty_requests_list(self,  address_list):
         
        # smarty "Batch" object to hold multi-address request 
        single_request_batch_partition = Batch()
        addresses_per_request = 0
        request_list = []
        for address in address_list:
            
            if addresses_per_request == SmartyAddressService.MAX_ADDRESSES_PER_REQUEST:
                request_list.append(single_request_batch_partition)
                single_request_batch_partition = Batch()
                addresses_per_request = 0
                

            # Lookup is smarty object for address lookup
            single_request_batch_partition.add(Lookup(address.input_string))
            addresses_per_request+=1
     
        if addresses_per_request>0:
            request_list.append(single_request_batch_partition)
        return request_list
        

    def validate(self, params, address_input_data):
        request_list = self.prepare_smarty_requests_list(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_list: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    address.is_valid = 'false'
                    print(f'{address.input_string} is invalid')
                else:
                    address.line_1 = candidates[0].delivery_line_1
                    address.line_2 = candidates[0].last_line
                    address.is_valid = 'true'
                processed_address_list.append(address)    
        return processed_address_list          


    def geocode(self, params, address_input_data ):
        request_list = self.prepare_smarty_requests_list(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_list: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    #TODO: is making this false correct behaviour?
                    address.is_valid = 'false'
                    print(f'{address.input_string} is invalid')
                else:
                    address.longitude = candidates[0].metadata.longitude
                    address.latitude = candidates[0].metadata.latitude
                processed_address_list.append(address)    
        return processed_address_list

    #TODO: combine above functions into this one, and break up this function/above ones w helpers 
    def validate_and_geocode(self, params, address_input_data ):
        request_list = self.prepare_smarty_requests_list(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_list: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    address.is_valid = 'false'
                    print(f'{address.input_string} is invalid')
                else:
                    address.longitude = candidates[0].metadata.longitude
                    address.latitude = candidates[0].metadata.latitude
                    address.line_1 = candidates[0].delivery_line_1
                    address.line_2 = candidates[0].last_line
                    address.is_valid = 'true'
                processed_address_list.append(address)    
        return processed_address_list 


