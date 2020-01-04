import argparse, sys, os, csv, configparser

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

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

    api_credentials = get_api_credentials(args['config'])
    client = ClientBuilder(api_credentials).build_us_street_api_client()
    batch_list = create_batch_list(args["infile"])

    with open (args['outfile'], 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',', quotechar = "'" )
        for batch in batch_list:
            processed_batch = process_batch_with_service(batch,client)
            # address standardization/validation and standardization
            if args['geoval']: 
                create_geocoding_and_validation_csv(csvWriter, processed_batch)
            # address geocoding only 
            elif args['geocode']:
                create_geocoding_csv( csvWriter, processed_batch )  
            # address address standardization/validation
            else:
                create_validation_csv( csvWriter, processed_batch )


# helper for connecting to API
def get_api_credentials(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    auth_id = config.get('ADDRESS SERVICE', 'id' )
    auth_token = config.get('ADDRESS SERVICE', 'key')
    credentials = StaticCredentials(auth_id, auth_token)
    return credentials

# helper for batch processing 
def create_batch_list(infile):
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        batch_list = []
        # pass over first line w column info 
        # TODO: use logic here for stream vs batch 
        try:
            csvReader.__next__() 
        except StopIteration as err:
            print(err)
            print("ensure input file not empty")
        
        batch = Batch() 
        for row in csvReader:
            address = str(row[0])

            if batch.__len__() == batch.MAX_BATCH_SIZE:
                batch_list.append(batch)
                batch = Batch()
        
            # TODO: change condition 
            if len(address)>10:
                batch.add(Lookup(address))

        if batch.__len__()>0:
            batch_list.append(batch)
    return batch_list

# helper for batch processing
def process_batch_with_service( batch, client):
    try:
        client.send_batch(batch)
        return batch
    except exceptions.SmartyException as err:
        print(err)
        return

# helper for geocoding output
def create_geocoding_csv( csvWriter, processed_batch):
    csvWriter.writerow(['address', 'latitude', 'longitude'])
    for lookup in processed_batch:
        candidates = lookup.result
        if len(candidates) == 0:
            csvWriter.writerow(['\"{}\"'.format(lookup.street), "", ""])
            print("Address {} is invalid".format(lookup.street))
        else:
            csvWriter.writerow(['\"{}\"'.format(lookup.street), candidates[0].metadata.latitude, candidates[0].metadata.longitude])

# helper for address validation output
def create_validation_csv( csvWriter, processed_batch):
    # TODO: Incorporate returned correction codes if want to return whether given address is truly valid( if it matters ) 
    # TODO: if delivery line >50 characters ?
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])
    for lookup in processed_batch:
        candidates = lookup.result
        if len(candidates) == 0:
            csvWriter.writerow(['\"{}\"'.format(lookup.street), "false",""])
            print("Address {} is invalid".format(lookup.street))
        else:
            csvWriter.writerow(['\"{}\"'.format(lookup.street),"true", "{}, {}".format(candidates[0].delivery_line_1, candidates[0].last_line)])

# helper for geocoding and address validation/standardization output
def create_geocoding_and_validation_csv(csvWriter, processed_batch):
    csvWriter.writerow(['address', 'is_valid', 'corrected_address', 'latitude', 'longitude'])
    for lookup in processed_batch:
        candidates = lookup.result
        if len(candidates) == 0:
            csvWriter.writerow(['\"{}\"'.format(lookup.street), "false","", "", ""])
            print("Address {} is invalid".format(lookup.street))
        else:
            csvWriter.writerow(['\"{}\"'.format(lookup.street),"true", "{}, {}".format(candidates[0].delivery_line_1,
                 candidates[0].last_line), candidates[0].metadata.latitude, candidates[0].metadata.longitude])
    
    

if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="provider address handler")
    arg_parser.add_argument('--config', nargs='?', default=None, required=True, 
        help='specified output file required')
    arg_parser.add_argument('--infile', nargs='?', default=None, required=True, 
        help='infile csv file with provider data, in a single address column')
    arg_parser.add_argument('--outfile', nargs='?', default=None, required=True, 
        help='specified output file required')
    arg_parser.add_argument('--geocode', nargs='?', default=False, required=False, 
        help='adding this argument enables forward address geocoding')
    arg_parser.add_argument('--geoval', nargs='?', default=False, required=False, 
        help='adding this argument combines address validation/standardization and geocoding')

    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)
