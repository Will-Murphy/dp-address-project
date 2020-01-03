import argparse, sys, os, csv, configparser

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

'''
# Sample usage
python formatted input.  
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
 

def run_batch(args=None):

    # API Authenticaion
    config = configparser.ConfigParser()
    config.read(args['config'])
    auth_id = config.get('ADDRESS SERVICE', 'id' )
    auth_token = config.get('ADDRESS SERVICE', 'key')
   
    # Connect to and Initialize Service
    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_street_api_client()
    batch = Batch()
    MAX_BATCH_SIZE = 100

    # open input csv
    # potentially split all lines at first 
    address_list = []
    with open (args['infile'], newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        # pass over first line w column info
        
        try:
            csvReader.__next__() 
        except StopIteration as err:
            print(err)
            print("ensure input file not empty")
    
        for row in csvReader:
            address = row[0]
            if len(address)>5:
                batch.add(Lookup(address))
                address_list.append(address)

    assert len(batch) == len(address_list)

    try:
        client.send_batch(batch)
    except exceptions.SmartyException as err:
        print(err)
        return
    
     
    with open (args['outfile'], 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',' )
        
        if args['geocode']:
            csvWriter.writerow(['address', 'latitude', 'longitude'])
            for i, lookup in enumerate(batch):
                candidates = lookup.result
                if len(candidates) == 0:
                    csvWriter.writerow([address_list[i], "null", "null"])
                    print("Address {} is invalid".format(address_list[i]))
                else:
                    csvWriter.writerow(["{}".format(str(address_list[i])), candidates[0].metadata.latitude, candidates[0].metadata.longitude])
        else: 
            csvWriter.writerow(['address', 'is_valid', 'corrected_address'])
            for i, lookup in enumerate(batch):
                candidates = lookup.result
                if len(candidates) == 0:
                    csvWriter.writerow([address_list[i], "false"])
                    print("Address {} is invalid".format(address_list[i]))
                else:
                    csvWriter.writerow(["{}".format(str(address_list[i])),"true", "{}, {}".format(candidates[0].delivery_line_1, candidates[0].last_line)])

        '''      
        print("Address {} is valid. (There is at least one candidate)".format(i))

        for candidate in candidates:
            components = candidate.components
            metadata = candidate.metadata

            print("\nCandidate {} : ".format(candidate.candidate_index))
            print("Delivery line 1: {}".format(candidate.delivery_line_1))
            print("Last line:       {}".format(candidate.last_line))
            print("ZIP Code:        {}-{}".format(components.zipcode, components.plus4_code))
            print("County:          {}".format(metadata.county_name))
            print("Latitude:        {}".format(metadata.latitude))
            print("Longitude:       {}".format(metadata.longitude))
        print("")
        '''      
        
    


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
        help='adding this argument enables geocoding')

    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)
