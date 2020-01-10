import csv 
from address import Address

"""
Input/output utilities to help address service class read and produce csv files
"""

############ Functions to read from csv input files ############# (make a class?)
def read_address_input(infile):
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        try:
            csvReader.__next__() 
        except StopIteration:
            print("\n Error: ensure input file not empty \n")
            raise 
        address_object_list = []
        for row in csvReader:
            address_string = str(row[0])
            #TODO:change condition
            if len(address_string)>10: 
                address = Address()
                address.input_string = address_string
                address_object_list.append(address)   
    return address_object_list

def read_coordinate_input(infile): 
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        try:
            csvReader.__next__() 
        except StopIteration:
            print("\n Error: ensure input file not empty \n")
            raise 
        address_object_list = []
        for row in csvReader:
            latitude = str(row[0])
            longitude = str(row[1])
            #TODO:change condition
            if len(latitude)>0 and len(longitude)>0: 
                address = Address()
                address.latitude = latitude
                address.longitue = longitude   
    return address_object_list
    

############ Functions to write to csv output files ############# (make a class?)
def write_forward_geocode_csv_output(processed_address_list, outfile):
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        __write_forward_geocode_header(csvWriter)
        for address in processed_address_list:
            __write_forward_geocode_data(csvWriter, address)
   

def write_validation_csv_output(processed_address_list, outfile): 
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        __write_validation_header(csvWriter)
        for address in processed_address_list:
            __write_validation_data(csvWriter, address)

def write_general_csv_output(processed_address_list, outfile): 
   with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        __write_general_header(csvWriter)
        for address in processed_address_list:
            __write_general_data(csvWriter, address)


# helpers for csv writing functions 

def __write_forward_geocode_header(csvWriter):
    csvWriter.writerow(['address', 'latitude', 'longitude'])

def __write_forward_geocode_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.latitude,
                        address.longitude ])


def __write_validation_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])

def __write_validation_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.is_valid,
                        f'{str(address.line_1)}, {str(address.line_2)}' ])


def __write_general_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address', 'latitude', 'longitude'])

def __write_general_data(csvWriter, address):
    csvWriter.writerow([f'{str(address.input_string)}',
                        address.is_valid,
                        f'{str(address.line_1)}, {str(address.line_2)}',
                        address.latitude,
                        address.longitude ])

def __write_reverse_geocode_header (csvWriter):
    csvWriter.writerow(['latitude', 'longitude', 'address'])

def __write_reverse_geocode_data  (csvWriter, address):
    csvWriter.writerow([f'{str(address.line_1)}',
                        address.latitude,
                        address.longitude ])