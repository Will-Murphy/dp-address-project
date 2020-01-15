import configparser
 
from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

from models.address import Address
from models.address_service import AddressService

class SmartyAddressService (AddressService):
    """
    Class represents Smarty Streets US_STREETS_API validatation and forward geocoding specific implementation AddressService class

    It implements that abstract class with helper methods that deal with its specific API implmentation.
    """

    MAX_ADDRESSES_PER_REQUEST = 100 

    def __init__(self):
        self.client = None 
        self.num_addresses_processed = 0
        self.__total_addresses_in_request_list = 0
        self.__is_address_list_processed = False


    def load_config(self, config_file):
        """ Resonsible for loading configs and setting up client """
        config = configparser.ConfigParser()
        config.read(config_file)
        auth_id = config.get('SMARTY STREETS', 'auth_id' )
        auth_token = config.get('SMARTY STREETS', 'auth_token')
        api_credentials = StaticCredentials(auth_id, auth_token)
        self.client = ClientBuilder(api_credentials).build_us_street_api_client()


    def send_request(self, params, address_data):
        """ Responsible for sending request to service and returning processed data """
        try:
            # Stream considered a batch of one
            self.client.send_batch(address_data)
            return address_data
        except exceptions.SmartyException as err:
            print(err)
            return
    

    def validate(self, params, address_input_data):
        """ 
        Reponsible for validating input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input and multiple for batch input.
        """
        processed_address_list = []
        # check avoids redundancy for combined 'forward geocode and validate' as API does both by default
        if self.__is_address_list_processed:
            processed_address_list = address_input_data
        else:
            request_list = self.__prepare_smarty_request_list(address_input_data)
            processed_address_list = self.__process_smarty_request_list(request_list,address_input_data )
            self.__is_address_list_processed = True
            print(f'< {self.num_addresses_processed} addresses processed >')
        return processed_address_list


    def forward_geocode(self, params, address_input_data ):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input and multiple for batch input.
        """
        processed_address_list = []
        # check avoids redundancy for combined 'forward geocode and validate' as API does both by default
        if self.__is_address_list_processed:
            processed_address_list = address_input_data
        else:
            request_list = self.__prepare_smarty_request_list(address_input_data)
            processed_address_list = self.__process_smarty_request_list(request_list, address_input_data )
            self.__is_address_list_processed = True
            print(f'< {self.num_addresses_processed} addresses processed >')
        return processed_address_list
        

    def reverse_geocode(self, params, coordinate_input_data):
        """ 
        Smarty Streets API does not support reverse geocoding
        """
        raise NotImplementedError(f'{type(self).__name__} does not provide this service')
    

    ############ Smarty Processing Helpers ############
    def __prepare_smarty_request_list(self, address_list):
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
            self.__total_addresses_in_request_list += 1
            addresses_per_request+=1
            
        if addresses_per_request>0:
            request_list.append(single_request_batch_partition)
        return request_list

    
    # TODO: python boolean or string for is_valid parameter?
    def __process_smarty_request_list(self, request_list, address_input_data ):
        """
        Process address input data contained in request list through smarty streets API

        Each individual request contains SmartyAddressService.MAX_ADDRESSES_PER_REQUEST address Lookups,
        which are assigned candidate addresses by their api. This function chooses the top candidate is chosen 
        and assigns desired fields to our address objects. If no candidates are found, the address is invalid. 
        """
        assert(len(address_input_data) == self.__total_addresses_in_request_list)

        processed_address_list = []
        address_iterator = iter(address_input_data)
        for unprocessed_request in request_list: 
            params = {}
            processed_request = self.send_request(params, unprocessed_request)
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
                self.num_addresses_processed+=1
                processed_address_list.append(address)  
        return processed_address_list 
            

            

         
      



