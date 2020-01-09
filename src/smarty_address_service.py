import configparser
import io_utilities

from address_service_class import AddressService
from address_class import Address

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

class SmartyAddressService (AddressService):
    
    def __init__(self):
        self.MAX_ADDRESSES_PER_REQUEST = 100 
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
    def format_request(self,  address_data = []):
        requests_in_batch = []
        single_request_data = Batch() 
        for address in address_data:
            address = str(address)

            if single_request_data.__len__() == self.MAX_ADDRESSES_PER_REQUEST:
                requests_in_batch.append(single_request_data)
                single_request_data = Batch()
    
            single_request_data.add(Lookup(address))

        if single_request_data.__len__()>0:
            requests_in_batch.append(single_request_data)
        return requests_in_batch
        

    def validate(self, params):
        address_input_data = io_utilities.read_address_input(params['infile'])
        request_batch = self.format_request(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_batch: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    address.is_valid = False
                    print(f'{address.input_string} is invalid')
                else:
                    address.line_1 = candidates[0].delivery_line_1
                    address.line_2 = candidates[0].last_line
                    address.is_valid = True
            processed_address_list.append(address)    
        io_utilities.write_validation_csv_output(processed_address_list, params["outfile"])            


    def geocode(self, params):
        address_input_data = io_utilities.read_address_input(params['infile'])
        request_batch = self.format_request(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_batch: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    #TODO: is making this false correct behaviour?
                    address.is_valid = False
                    print(f'{address.input_string} is invalid')
                else:
                    address.longitude = candidates[0].metadata.longitude
                    address.latitude = candidates[0].metadata.latitude
            processed_address_list.append(address)    
        io_utilities.write_geocode_csv_output(processed_address_list, params["outfile"]) 
 
    #TODO: combine above functions into this one, and break up this function/above ones w helpers 
    def validate_and_geocode(self, params):
        address_input_data = io_utilities.read_address_input(params['infile'])
        request_batch = self.format_request(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_batch: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                print(candidates)
                address = Address()
                address.input_string = lookup.street
                if len(candidates) == 0:
                    address.is_valid = False
                    print(f'{address.input_string} is invalid')
                else:
                    address.longitude = candidates[0].metadata.longitude
                    address.latitude = candidates[0].metadata.latitude
                    address.line_1 = candidates[0].delivery_line_1
                    address.line_2 = candidates[0].last_line
                    address.is_valid = True
            processed_address_list.append(address)    
        io_utilities.write_general_csv_output(processed_address_list, params["outfile"]) 




