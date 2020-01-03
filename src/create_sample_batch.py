import csv, sys, argparse

'''
generate batch

usage: python generate_sample_batch BATCH_SIZE

'''
def run(args=None):
    create_batch(args)


def create_batch(args=None):
    with open ('../npi-sample-data/npi_data_dec_2019.csv', newline = '') as csv_infile, open('../npi-sample-data/npi_small_batch.csv', 'w', newline = '') as csv_outfile_test:
        csvReader = csv.DictReader(csv_infile, delimiter = ',')
        csvWriter = csv.writer(csv_outfile_test, delimiter =',')
        csvWriter.writerow(["address"])
        count = 1
        while count < int(args["batchsize"]):
            row = csvReader.__next__()
            line1 = row["Provider First Line Business Practice Location Address"]
            line2 = row["Provider Second Line Business Practice Location Address"]
            city =  row["Provider Business Practice Location Address City Name"]
            state = row["Provider Business Practice Location Address State Name"]
            zip  = row["Provider Business Practice Location Address Postal Code"]
            address_str = line1 +' ' +  line2 +' '+ city + ' ' +  state +' ' + zip 
            if count%10 == 0  and len(address_str)>=7:
                csvWriter.writerow([address_str])
                print( address_str, len(address_str) ) 
            count += 1


if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="Helper for querying a database.")
    arg_parser.add_argument('--batchsize', nargs='?', default=100, required=False, 
        help='specify batch size')
    
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)