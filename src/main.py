import argparse, sys, os, csv
import io_utilities

from smarty_address_service import SmartyAddressService
'''
# Sample usage
python3 provider_address.py provider_address.py --config [CONFIG] --infile [INFILE] --outfile
                           [OUTFILE] [--geocode [GEOCODE]] [--geoval [GEOVAL]]
# Notes:
#  - Third Party GeoCoding and Address Valdiation Service: Smarty Streets 
#  - Will probably desgin such that run batch can decide about stream or batch input and handle it
#    nearly identically
#
# SMARTY STREET specific notes: 
#  - MAX_BATCH_SIZE = 100 lookups/request
#  - "freeform" input address is saved in the smarty streets 'Lookup' object in the 'street' attribute
#  - Later use potentially address opensource lib for problem "freeform" inputs, or altogether
'''
 
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
def run_one(args=None):
    pass
    # implementation
    # can adapt batch handling for this

def run_batch(args=None):

    address_service = SmartyAddressService()
    address_service.load_config(args['config'])
    
    # Standardization/Validation and geocoding 
    if int(args['options']) == 0: 
        address_service.validate_and_geocode(args)
    # Geocoding only 
    elif int(args['options']) == 1:
        address_service.geocode(args)
    # Standardization/Validation only 
    elif int(args['options']) == 2:
        address_service.validate(args)
    

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
