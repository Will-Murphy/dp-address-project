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
        address_list = []
        try:
            csvReader.__next__() 
        except StopIteration as err:
            print(err)
            print("ensure input file not empty")

        for row in csvReader:
            address = str(row[0])
            #TODO:change condition
            if len(address)>10: 
                address_list.append(address)   
    return address_list


# helpers for writing csv GEOCODING output headers 
def write_geocode_header(csvWriter):
    csvWriter.writerow(['address', 'latitude', 'longitude'])

def write_geocode_data(csvWriter, address):
    csvWriter.writerow([f'\"{str(address.input_string)}\"',
                        address.latitude,
                        address.longitude ])

# helpers for writing csv VALIDATION output headers 
def write_validation_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])

def write_validation_data(csvWriter, address):
    csvWriter.writerow([f'\"{str(address.input_string)}\"',
                        address.is_valid,
                        f'\"{str(address.line_1)} {str(address.line_2)}\"' ])
   
# helpers for writing csv GEOCODING & VALIDATION output headers 
def write_general_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address', 'latitude', 'longitude'])

def write_general_data(csvWriter, address):
    csvWriter.writerow([f'\"{str(address.input_string)}\"',
                        address.is_valid,
                        f'\"{str(address.line_1)} {str(address.line_2)}\"',
                        address.latitude,
                        address.longitude ])


### Functions called by address service classes once they process addresses ###
                   
def write_geocode_csv_output(processed_address_list, outfile):
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',', quotechar = "'" )
        write_geocode_header(csvWriter)
        for address in processed_address_list:
            write_geocode_data(csvWriter, address)
   

def write_validation_csv_output(processed_address_list, outfile): 
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',', quotechar = "'" )
        write_validation_header(csvWriter)
        for address in processed_address_list:
            write_validation_data(csvWriter, address)

def write_general_csv_output(processed_address_list, outfile): 
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',', quotechar = "'" )
        write_general_header(csvWriter)
        for address in processed_address_list:
            write_general_data(csvWriter, address)