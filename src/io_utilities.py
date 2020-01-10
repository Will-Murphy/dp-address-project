import csv 
from address import Address


'''
Input/output utilities to help address service class read and produce csv files
'''

# helper for reading csv address input 
# TODO: merge input list with address object read in from service
# maybe make this a class and have is save a list of address objects 
def read_address_input(infile):
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        address_object_list = []
        try:
            csvReader.__next__() 
        except StopIteration as err:
            print(err)
            print("ensure input file not empty")

        for row in csvReader:
            address_string = str(row[0])
            #TODO:change condition
            if len(address_string)>10: 
                address = Address()
                address.input_string = address_string
                address_object_list.append(address)   
    return address_object_list


### Functions called by address service classes once they process addresses ###                
def write_geocode_csv_output(processed_address_list, outfile):
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        _write_geocode_header(csvWriter)
        for address in processed_address_list:
            _write_geocode_data(csvWriter, address)
   

def write_validation_csv_output(processed_address_list, outfile): 
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        _write_validation_header(csvWriter)
        for address in processed_address_list:
            _write_validation_data(csvWriter, address)

def write_general_csv_output(processed_address_list, outfile): 
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        _write_general_header(csvWriter)
        for address in processed_address_list:
            _write_general_data(csvWriter, address)


### helpers for respective csv writing functions above ###
def _write_geocode_header(csvWriter):
    csvWriter.writerow(['address', 'latitude', 'longitude'])

def _write_geocode_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.latitude,
                        address.longitude ])


def _write_validation_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])

def _write_validation_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.is_valid,
                        f'{str(address.line_1)}, {str(address.line_2)}' ])


def _write_general_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address', 'latitude', 'longitude'])

def _write_general_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.is_valid,
                        f'{str(address.line_1)}, {str(address.line_2)}',
                        address.latitude,
                        address.longitude ])