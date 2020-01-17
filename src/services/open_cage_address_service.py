import configparser

from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

from models.address import Address
from models.address_service import AddressService
 
class OpenCageAddressService (AddressService):
    """
    Class represents Open Cage implementation of AddressService class. It 
    provides reverse and forward geocoding. 

    Open cage is rate limited based on API access tier, so request 
    response time will be variable. 
    """ 
    
    def __init__(self):
        self.client = None
        self.num_addresses_processed = 0 

    def load_config(self, config_file):
        """Resonsible for loading configs and setting up client"""
        config = configparser.ConfigParser()
        config.read(config_file)
        auth_key = config.get('OPEN CAGE', 'auth_key' )
        self.client = OpenCageGeocode(auth_key)

    def send_request(self, params,  address_data):
        """Responsible for sending a request to service"""
        try:
            # forward geocoding 
            if int(params["options"]) == 2: 
                address_query = u'{address_data.input_string}'
                results = self.client.geocode(address_query)
                print(f'{type(self).__name__} request sent.' \
                       'Waiting on rate limit...')
                return results
            # reverse geocoding 
            elif int(params["options"]) == 3:
                latitude = address_data.latitude
                longitude = address_data.longitude
                results = self.client.reverse_geocode(latitude, 
                                                    longitude, 
                                                    language = 'eng', 
                                                    no_annotations='1')
                print(f'<{type(self).__name__} request sent.' \
                       'Waiting on rate limit...>')
                return results
        except RateLimitExceededError as rate_err:
            print(rate_err)
        except UnknownError as unkwn_err:
            print("\n Error: An unspecified server issue occured \n")
            print(unkwn_err)
        except InvalidInputError as invalid_err:
            print(invalid_err)
            raise
        
    def forward_geocode(self, params, address_input_data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input 
        and multiple for batch input.
        """
        processed_address_list = []
        for address in address_input_data: 
            result = self.send_request(params, address)
            self.num_addresses_processed += 1
            if result and len(result):
                address.latitude = result[0]['geometry']['lat']
                address.longitude = result[0]['geometry']['lng']
                address.is_valid = True
            else: 
                address.is_valid = False
            processed_address_list.append(address)

        print(f'< {self.num_addresses_processed} addresses processed >')
        return processed_address_list
    
    def reverse_geocode(self, params, address_input_data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input 
        and multiple for batch input.
        """
        processed_address_list = []
        for address in address_input_data: 
            result = self.send_request(params, address)
            self.num_addresses_processed += 1
            if result and len(result):
                address.line_1 = result[0]['formatted']
                address.is_valid = True
            else: 
                address.is_valid = False
            processed_address_list.append(address)

        print(f'< {self.num_addresses_processed} addresses processed >')
        return processed_address_list
        
     