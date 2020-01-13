from ..models.address import Address


############ Functions to read input strings ############# (make a class?)
def read_address_input(address_string): 
    assert len(str(address_string)) > 0, "address input should be a string of nonzero length"
    
    address = Address() 
    address.input_string = address_string
    return address

def read_coordinate_input(coordinate_string): 
    coordinates = coordinate_string.split(",")
    assert len(coordinates) == 2, " coordinate input should be a string as follows '<latitude>, <longitude>' "

    address = Address() 
    address.latitude = coordinates[0].strip() 
    address.longitude = coordinates[1].strip()
    return address

############ Functions to constuct output strings ############# (make a class?)
def construct_geocode_and_validiation_output( address_object):
    return vars(address_object)

def construct_validation_output( address_object ):
    return vars(address_object)

def construct_geocode_output( address_object ): 
    return vars(address_object)

def construct_reverse_geocode_output( address_object): 
    return vars(address_object)





    
    
