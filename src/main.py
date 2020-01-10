import argparse, sys
import io_utilities

from smarty_address_service import SmartyAddressService
from open_cage_address_service import OpenCageAddressService

#TODO: fix file structure, implement stream 
        
'''
# Sample usage
python3 provider_address.py provider_address.py --config [CONFIG] --infile [INFILE] --outfile
                           [OUTFILE] [--options [OPTIONS]]
'''

#TODO: add logic for run one 
def run(args=None):
    if not args:
        return
    else:
        run_batch(args=args)
   
# TODO: implement this method
def run_one(args=None):
    pass

#TODO: make logic operations ordering more logical
def run_batch(args=None):

    address_service = SmartyAddressService()
    address_service.load_config(args['config'])

    address_service_2 = OpenCageAddressService()
    address_service_2.load_config(args['config'])
    
    # Geocode and validate 
    if int(args['options']) == 0: 

        input_address_list = io_utilities.read_address_input(args["infile"])
        validated_address_list = address_service.validate(args, input_address_list)
        processed_address_list = address_service.forward_geocode(args, validated_address_list)
        io_utilities.write_general_csv_output(processed_address_list, args['outfile'] )
    
    # Geocode 
    elif int(args['options']) == 1:

        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.forward_geocode(args, input_address_list)
        io_utilities.write_forward_geocode_csv_output(processed_address_list, args['outfile'] )

    # Validate
    elif int(args['options']) == 2:

        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.validate(args, input_address_list)
        io_utilities.write_validation_csv_output(processed_address_list, args['outfile'] )
    
    # Reverse Geocode 
    elif int(args['options']) == 3:

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
    arg_parser.add_argument('--options', nargs='?', default=0, required=False, 
        help='options to choose what program outputs')
    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)
