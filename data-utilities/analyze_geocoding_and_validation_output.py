import csv, sys, argparse

'''
Print stats on outputted file from dp-address-project option 0

usage: 
    python analyze_geocoding_and_validation_output.py --infile ../sample-input-output/forward_geocoding_and_validation_output.csv 

        
'''
def run(args=None):
    analyze_output(args)


#TODO: clean up this method 
def analyze_output(args):
    with open (args['infile'], newline = '') as csv_infile:
        csvReader = csv.DictReader(csv_infile, delimiter = ',')
        row = csvReader.__next__()

        validated_count = 0 
        geocoded_count = 0 
        total_address_count = 0
        try: 
            while True: 
                
                is_address_valid = bool(row["is_valid"])
                is_address_geocoded = len(str(row["latitude"])) and len(str(row["longitude"]))

                if is_address_valid: validated_count += 1 
                if is_address_geocoded: geocoded_count += 1
                total_address_count += 1

                row = csvReader.__next__()

                
            
        except StopIteration as err:
            print(err)
        
        finally: 
           log_validation_and_geocoding_output_stats( validated_count, geocoded_count, total_address_count)
 
        

            

def log_validation_and_geocoding_output_stats( validated_count, geocoded_count, total_address_count):
    print(f'validated {validated_count} out of {total_address_count} addresses, or {validated_count/total_address_count} percent')
    print(f'geocoded {geocoded_count} out of {total_address_count} addresses, or {geocoded_count/total_address_count} percent')


if __name__ == '__main__':
    # Define available arguments
    arg_parser = argparse.ArgumentParser(description="Helper for querying a database.")
    arg_parser.add_argument('--infile', nargs='?', default='', required=False, 
        help='input npi csv file')
    
    # Get variables from the arguments
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    
    print(f'args: {args}')
 
    run(args)