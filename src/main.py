import argparse, sys
import io_utilities

from smarty_address_service import SmartyAddressService

#TODO: fix file structure, implement stream 
        
'''
# Sample usage
python3 provider_address.py provider_address.py --config [CONFIG] --infile [INFILE] --outfile
                           [OUTFILE] [--options [OPTIONS]]
# Notes:
 - Third Party GeoCoding and Address Valdiation Service: Smarty Streets 
 - Will probably desgin such that run batch can decide about stream or batch input and handle it
   nearly identically

# SMARTY STREET specific notes: 
 - MAX_BATCH_SIZE = 100 lookups/request
 - "freeform" input address is saved in the smarty streets 'Lookup' object in the 'street' attribute
 - Later use potentially address opensource lib for problem "freeform" inputs, or altogether
'''
#TODO: add logic for run one 
def run(args=None):
    if not args:
        return
    else:
        run_batch(args=args)
    '''
    if args['batchsize']:
        run_batch(args=args)
    else:
        run_one(args=args)
    '''
# TODO: implement this method
def run_one(args=None):
    pass
    
def run_batch(args=None):

    address_service = SmartyAddressService()
    address_service.load_config(args['config'])
    
    if int(args['options']) == 0: 
        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.validate_and_geocode(args, input_address_list)
        io_utilities.write_general_csv_output(processed_address_list, args['outfile'] )

    elif int(args['options']) == 1:
        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.geocode(args, input_address_list)
        io_utilities.write_general_csv_output(processed_address_list, args['outfile'] )

    elif int(args['options']) == 2:
        input_address_list = io_utilities.read_address_input(args["infile"])
        processed_address_list = address_service.validate(args, input_address_list)
        io_utilities.write_general_csv_output(processed_address_list, args['outfile'] )
    
    else: 
        print("options parameter takes number 0-2")
    

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
