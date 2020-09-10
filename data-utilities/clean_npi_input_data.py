import csv, sys, argparse

'''
Generate batch ready to be ingested by dp-address-project main script. 

Writes out to a file called sample_address_input.csv

usage: 

       python clean_npi_input_data.py --batchsize 10 --infile ../npi-sample-data/npi_full_dataset_sept_2020.csv --outfile out.csv

'''
def run(args=None):
    create_cleaned_batch(args)


#TODO: clean up this method 
def create_cleaned_batch(args):
    with open (args['infile'], newline = '') as csv_infile, \
         open(args['outfile'], 'w', newline = '') as csv_outfile_test:
        csvReader = csv.DictReader(csv_infile, delimiter = ',')
        csvWriter = csv.writer(csv_outfile_test)
        csvWriter.writerow(["address"])
        total_address_count = 0
        batch_size = 0
        while total_address_count < int(args["batchsize"]):
            try:
                row = csvReader.__next__()
                line1 = row["Provider First Line Business Practice Location Address"]
                line2 = row["Provider Second Line Business Practice Location Address"]
                city =  row["Provider Business Practice Location Address City Name"]
                state = row["Provider Business Practice Location Address State Name"]
                zip_code  = row["Provider Business Practice Location Address Postal Code"]
                
                address_str = get_addr_str_from_npi_data(line1, line2, city, state, zip_code)
                total_address_count += 1

                if address_str is not None:
                    csvWriter.writerow([f'{str(address_str)}'])
                    batch_size += 1
                     
            except StopIteration as err:
                print(err)
                log_cleaned_batch_statistics(batch_size, total_address_count)
                
        log_cleaned_batch_statistics(batch_size, total_address_count)

def get_addr_str_from_npi_data(line1, line2, city, state, zip_code):
    """ Return formatted address input string from npi csv data, 
        or None if address fields are emptyS
    """ 
    if len(line1) <= 0:
        address_str = None 
    elif len(line2) <= 0:
        address_str = line1 +', ' + city + ', ' +  state +' ' + zip_code
    else: 
        address_str = line1 +', ' +  line2 +', '+ city + ', ' +  state +' ' + zip_code
    
    return address_str

def log_cleaned_batch_statistics(batch_size, total_address_count):
    print(f'{batch_size} valid NPI addresses added to batch out of {total_address_count} from NPI file')



if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="Helper for querying a database.")
    arg_parser.add_argument('--batchsize', nargs='?', default=100, required=False, 
        help='specify batch size')
    arg_parser.add_argument('--infile', nargs='?', default='../npi-sample-data/npi_data_dec_2019.csv', required=False, 
        help='input npi csv file')
    arg_parser.add_argument('--outfile', nargs='?', default='../sample-input-output/sample_address_input.csv', required=False, 
        help='input npi csv file')
    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)