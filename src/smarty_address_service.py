import configparser

from address_service import AddressService
from address import Address

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

class SmartyAddressService (AddressService):
    """
    Class represents smarty Streets US_STREETS_API Specific implementation of AddressService class. 

    It implements that abstract class with helper methods that deal with its specific API implmentation
    """

    MAX_ADDRESSES_PER_REQUEST = 100 

    # TODO: add number of processed addresses variable 
    def __init__(self):
        self.client = None 

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        auth_id = config.get('SMARTY STREETS', 'id' )
        auth_token = config.get('SMARTY STREETS', 'key')
        api_credentials = StaticCredentials(auth_id, auth_token)
        self.client = ClientBuilder(api_credentials).build_us_street_api_client()


    #TODO: clarify naming in this function, add parameters for stream logic
    def send_request(self, params, address_data):
        try:
            self.client.send_batch(address_data)
            return address_data
        except exceptions.SmartyException as err:
            print(err)
            return
    

    def validate(self, params, address_input_data):
        processed_address_list = []
        if self.__is_address_list_processed(address_input_data):
            processed_address_list = address_input_data
        else:
            request_list = self.__prepare_smarty_requests_list(address_input_data)
            processed_address_list = self.__smarty_process_address_input_data(request_list,address_input_data )
        return processed_address_list


    def forward_geocode(self, params, address_input_data ):
        processed_address_list = []
        if self.__is_address_list_processed(address_input_data):
            processed_address_list = address_input_data
        else:
            request_list = self.__prepare_smarty_requests_list(address_input_data)
            processed_address_list = self.__smarty_process_address_input_data(request_list,address_input_data )
        return processed_address_list
    

    def reverse_geocode(self, params, coordinate_input_data):
        raise NotImplementedError(f'{type(self).__name__} does not provide this service')


    
    ########### Smarty Batch Processing Helpers ###########
    def __is_address_list_processed(self, address_list):
        """
        Checks if address list has already been processed
         
        Used to avoid processing list twice, since smarty streets geocodes and validates in 
        the same request.  add note for logic 
        """
        # TODO: make this condition more robust
        if address_list[0].is_valid is None:
            return False
        else: 
            return True
    

    #TODO: add parameters for stream
    def __prepare_smarty_requests_list(self,  address_list):
        """
        Returns a list of requests each containing SmartyAddressService.MAX_ADDRESSES_PER_REQUEST
        address input strings.
        
        Input Address strings are converted  smarty street Lookup objects. 
        The request list is a list of batch partitions, smarty street Batch objects, which serves 
        as the overall address batch. 
        """
        single_request_batch_partition = Batch()
        addresses_per_request = 0
        request_list = []
        for address in address_list:
            if addresses_per_request == SmartyAddressService.MAX_ADDRESSES_PER_REQUEST:
                request_list.append(single_request_batch_partition)
                single_request_batch_partition = Batch()
                addresses_per_request = 0
            single_request_batch_partition.add(Lookup(address.input_string))
            addresses_per_request+=1

        if addresses_per_request>0:
            request_list.append(single_request_batch_partition)
        return request_list


    def __smarty_process_address_input_data(self,request_list, address_input_data ):
        """
        Process address input data contained in request list through smarty streets api


        Each individual request contains SmartyAddressService.MAX_ADDRESSES_PER_REQUEST address Lookups,
        which are assigned candidate addresses by their api. This function chooses the top candidate is chosen 
        and assigns desired fields to our address objects. If no candidates are found, the address is invalid. 
        """
        address_iterator = iter(address_input_data)
        processed_address_list = []
        for unprocessed_request in request_list: 
            request_params = {}
            processed_request = self.send_request(request_params, unprocessed_request)
            for lookup in processed_request:
                candidates = lookup.result
                address = next(address_iterator)
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
        return processed_address_list 

      



