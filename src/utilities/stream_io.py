from ..models.address import Address

"""
Stream input/output utilities for creating of dp-address stream endpoint. 

In order to resuse batch logic in address service classes, address and coordinates string inputs 
are converted into list containing a single address object, and from a list back into an address object
before being processed for output. 
"""

############ Functions to read input strings in address object list containing one address ############# 
def read_address_input(address_string): 
    #TODO: fix logic here for better input checking 
    assert len(str(address_string)) > 0, "address input should be a string of nonzero length"
    address = Address() 
    address.input_string = address_string
    return __get_list_from_single_address(address)
    

def read_coordinate_input(coordinate_string): 
    coordinates = coordinate_string.split(",")
    #TODO: fix logic here for better input checking 
    assert len(coordinates) == 2, " coordinate input should be a string as follows '<latitude>, <longitude>' "
    address = Address() 
    address.latitude = coordinates[0].strip() 
    address.longitude = coordinates[1].strip()
    return __get_list_from_single_address(address)

############ Functions to constuct output strings from address list w/ one object ############# 
def construct_geocode_and_validiation_output( processed_address_list):
    processed_address = __get_single_address_from_list(processed_address_list)
    if processed_address.is_valid is True: 
        return f' "{processed_address.line_1}, {processed_address.line_2}", "{processed_address.latitude}, {processed_address.longitude}" '
    else:
        return f'{processed_address.input_string} is not valid'
       
def construct_validation_output( processed_address_list ):
    processed_address = __get_single_address_from_list(processed_address_list)   
    if processed_address.is_valid is True: 
        return f' "{processed_address.line_1}, {processed_address.line_2}"'
    else:
        return f'{processed_address.input_string} is not valid'

def construct_foward_geocode_output( processed_address_list ): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    if processed_address.is_valid is True: 
        return f"{processed_address.latitude, processed_address.longitude}"
    else:
        return f'{processed_address.input_string}  is not valid'

#TODO: standardize convention returned for error here.. none or false?
def construct_reverse_geocode_output( processed_address_list): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    if processed_address.line_1 is not None: 
        return f' "{processed_address.line_1}" '
    else:
        return f'coordinates:"{processed_address.latitude, processed_address.longitude}" are not valid'

############ Helpers convert address objects to and from list ############
def __get_list_from_single_address(address):
        return [address]
def __get_single_address_from_list(list): 
        return list[0]
                
    





    
    
