import argparse, sys

from services.open_cage_address_service import OpenCageAddressService
from services.smarty_address_service import SmartyAddressService
from utilities import stream_io

#TODO: fix file structure/import statement
        
"""
Entry point for stream processing of addresses. It prints & returns an 
output string.

see readme for usage details. 
"""

def run(args=None):

    address_service = SmartyAddressService()
    address_service.load_config(args['config'])

    address_service_2 = OpenCageAddressService()
    address_service_2.load_config(args['config'])

    if int(args['options']) == 0:
        print(f'< using {type(address_service).__name__}' 
               'for address validation and forward geocoding >')
        input_address = stream_io.read_address_input(args["input"])
        validated_address = address_service.validate(args, input_address)
        processed_address = address_service.forward_geocode(args, 
                                                            validated_address)
        output_string = stream_io.construct_geocode_and_validiation_output(
                                                            processed_address)
        print(output_string)
        return output_string
    
    elif int(args['options']) == 1:
        print(f'< using {type(address_service).__name__} for address validation >')
        input_address = stream_io.read_address_input(args["input"])
        processed_address = address_service.validate(args, input_address)
        output_string = stream_io.construct_validation_output(processed_address)
        print(output_string)
        return output_string
        
    elif int(args['options']) == 2:
        print(f'< using {type(address_service).__name__} for forward geocoding >')
        input_address = stream_io.read_address_input(args["input"])
        processed_address = address_service.forward_geocode(args, input_address)
        output_string = stream_io.construct_foward_geocode_output(processed_address)
        print(output_string)
        return output_string

    elif int(args['options']) == 3:
        print(f'< using {type(address_service_2).__name__} for reverse geocoding >')
        input_coordinate_list = stream_io.read_coordinate_input(args["input"])
        processed_address = address_service_2.reverse_geocode(args, 
                                                              input_coordinate_list)
        output_string = stream_io.construct_reverse_geocode_output(
                                                              processed_address)
        output_string = print(output_string)
        return output_string

    else: 
        print("options parameter takes number 0-3")
    

if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="provider address handler")
    arg_parser.add_argument('--config', nargs='?', default=None, required=True, 
        help='specified output file required')
    arg_parser.add_argument('--input', nargs='?', default=None, required=True, 
        help='')
    arg_parser.add_argument('--options', nargs='?', default=0, required=False, 
        help='options to choose what program outputs')
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)
