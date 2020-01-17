"""
Stream input/output utilities for creating of dp-address stream endpoint.
Responsible for creation of address objects from input. 

Note: In order to resuse batch logic in address service classes, address 
and coordinates string inputs are converted into list containing a single 
address object, and from a list back into an address object before being 
processed for output. 
"""
from models.address import Address

############ Functions to Read Input Strings  ############# 
def read_address_input(address_string): 
    assert len(str(address_string)) > 0, \
           "address input should be a string of nonzero length"
    address = Address() 
    address.input_string = address_string
    return __get_list_from_single_address(address)
    

def read_coordinate_input(coordinate_string): 
    coordinates = coordinate_string.split(",")
    assert len(coordinates) == 2, \
           "coordinate input should be a string as follows '<latitude>, <longitude>' "
    address = Address() 
    address.latitude = coordinates[0].strip() 
    address.longitude = coordinates[1].strip()
    return __get_list_from_single_address(address)



############ Functions to Constuct Output Strings ############# 
def construct_geocode_and_validiation_output( processed_address_list):
    processed_address = __get_single_address_from_list(processed_address_list)
    output_address = processed_address.get_standardized_string()
    output_coordinates = processed_address.get_coordinates_string()
    input_string = processed_address.input_string

    if processed_address.is_valid is True: 
        return f'"{output_address}", "{output_coordinates}"'       
    else:
        return f'address:"{input_string}" is invalid'


def construct_validation_output( processed_address_list ):
    processed_address = __get_single_address_from_list(processed_address_list)   
    output_address = processed_address.get_standardized_string()
    input_string = processed_address.input_string

    if processed_address.is_valid is True: 
        return f'"{output_address}"'
    else:
        return f'address:"{input_string}" is invalid'


def construct_foward_geocode_output( processed_address_list ): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    output_coordinates = processed_address.get_coordinates_string()
    input_string = processed_address.input_string

    if processed_address.is_valid is True: 
        return f'"{output_coordinates}"'       
    else:
        return f'address:"{input_string}" is invalid'


def construct_reverse_geocode_output( processed_address_list): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    output_address = processed_address.get_standardized_string()
    input_string =  processed_address.get_coordinates_string()
    
    if processed_address.is_valid is True: 
        return f'"{output_address}"'
    else:
        return f'coordinates:"{input_string}" is invalid'

############ Helpers Convert Address Objects to and From List ############
def __get_list_from_single_address(address):
        return [address]
def __get_single_address_from_list(list): 
        return list[0]
                
    





    
    
