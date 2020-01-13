import argparse, sys
import io_utilities

from smarty_address_service import SmartyAddressService
from open_cage_address_service import OpenCageAddressService

#TODO: fix file structure/import statements, implement stream 
        
'''
# Sample usage
python3 provider_address.py provider_address.py --config [CONFIG] --infile [INFILE] --outfile
                           [OUTFILE] [--options [OPTIONS]]
'''

def run(args=None):
    if not args:
        return
    elif (args['batch']):
        run_batch(args=args)
    else:
        run_one(args=args)
         

# TODO: implement this method
def run_one(args=None):
    pass


def run_batch(args=None):

    address_service = SmartyAddressService()
    address_service.load_config(args['config'])

    address_service_2 = OpenCageAddressService()
    address_service_2.load_config(args['config'])
    
    if int(args['options']) == 0:
        print(f'< using {type(address_service).__name__} for address validation and forward geocoding >')
        input_address_list = io_utilities.read_address_input(args["infile"])
        validated_address_list = address_service.validate(args, input_address_list)
        processed_address_list = address_service.forward_geocode(args, validated_address_list)
        io_utilities.write_general_csv_output(processed_address_list, args['outfile'] )
    
    elif int(args['options']) == 1:
        print(f'< using {type(address_service).__name__} for address validation >')
        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.validate(args, input_address_list)
        io_utilities.write_validation_csv_output(processed_address_list, args['outfile'] )

    elif int(args['options']) == 2:
        print(f'< using {type(address_service).__name__} for forward geocoding >')
        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.forward_geocode(args, input_address_list)
        io_utilities.write_forward_geocode_csv_output(processed_address_list, args['outfile'] )

    elif int(args['options']) == 3:
        print(f'< using {type(address_service_2).__name__} for reverse geocoding >')
        input_coordinate_list = io_utilities.read_coordinate_input(args["infile"])
        processed_address_list = address_service_2.reverse_geocode(args, input_coordinate_list)
        io_utilities.write_reverse_geocode_csv_output(processed_address_list, args['outfile'] )

    else: 
        print("options parameter takes number 0-3")
    


if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="provider address handler")
    arg_parser.add_argument('--config', nargs='?', default=None, required=True, 
        help='specified output file required')
    arg_parser.add_argument('--infile', nargs='?', default=None, required=True, 
        help='infile csv file with provider data, in a single address column')
    arg_parser.add_argument('--outfile', nargs='?', default=None, required=True, 
        help='specified output file required')
    arg_parser.add_argument('--batch', nargs='?', default=True, required=False, 
        help='specified output file required')
    arg_parser.add_argument('--options', nargs='?', default=0, required=False, 
        help='options to choose what program outputs')
    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)
