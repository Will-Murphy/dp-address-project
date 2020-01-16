from models.address import Address

#TODO: FIGURE OUT DESIRED OUTPUT FORMATTING AND UPDATE HERE 
"""
Stream input/output utilities for creating of dp-address stream endpoint. 

Note: In order to resuse batch logic in address service classes, address 
and coordinates string inputs are converted into list containing a single 
address object, and from a list back into an address object before being 
processed for output. 
"""

############ Functions to Read Input Strings  ############# 
def read_address_input(address_string): 
    #TODO: fix logic here for better input checking 
    assert len(str(address_string)) > 0, \
           "address input should be a string of nonzero length"
    address = Address() 
    address.input_string = address_string
    return __get_list_from_single_address(address)
    

def read_coordinate_input(coordinate_string): 
    coordinates = coordinate_string.split(",")
    #TODO: fix logic here for better input checking 
    assert len(coordinates) == 2, \
           "coordinate input should be a string as follows '<latitude>, <longitude>' "
    address = Address() 
    address.latitude = coordinates[0].strip() 
    address.longitude = coordinates[1].strip()
    return __get_list_from_single_address(address)



############ Functions to Constuct Output Strings ############# 
def construct_geocode_and_validiation_output( processed_address_list):
    processed_address = __get_single_address_from_list(processed_address_list)
    if processed_address.is_valid is True: 
        return f'"{processed_address.line_1}, {processed_address.line_2}", ' \
               f'"{processed_address.latitude}, {processed_address.longitude}"'
    else:
        return f'address:"{processed_address.input_string}" is invalid'


def construct_validation_output( processed_address_list ):
    processed_address = __get_single_address_from_list(processed_address_list)   
    if processed_address.is_valid is True: 
        return f' "{processed_address.line_1}, {processed_address.line_2}"'
    else:
        return f'address:"{processed_address.input_string}" is invalid'


def construct_foward_geocode_output( processed_address_list ): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    if processed_address.is_valid is True: 
        return f' "{processed_address.latitude}, {processed_address.longitude}" '
    else:
        return f'"{processed_address.input_string}" is invalid'


#TODO: standardize convention returned for error here.. none or false?
def construct_reverse_geocode_output( processed_address_list): 
    processed_address = __get_single_address_from_list(processed_address_list) 
    if processed_address.line_1 is not None: 
        return f' "{processed_address.line_1}" '
    else:
        return f'coordinates:"{processed_address.latitude}' \
               f', {processed_address.longitude}" are not valid'



############ Helpers Convert Address Objects to and From List ############
def __get_list_from_single_address(address):
        return [address]
def __get_single_address_from_list(list): 
        return list[0]
                
    





    
    
