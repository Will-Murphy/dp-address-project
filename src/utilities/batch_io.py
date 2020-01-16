import csv

from models.address import Address

#TODO: FIGURE OUT DESIRED OUTPUT FORMATTING AND UPDATE HERE 

"""
Input/output utilities to help address service class read and produce csv files 
"""

OUTPUT_CSV_NULL_STRING = ""
OUTPUT_CSV_FALSE = "FALSE"
OUTPUT_CSV_TRUE = "TRUE"

############ Functions to read from csv input files ############# 
def read_address_input(infile):
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        __check_address_input(csvReader)
        address_object_list = []
        for row in csvReader:
            address_string = str(row[0])
            #TODO:change condition based on actual input 
            if len(address_string)>10: 
                address = Address()
                address.input_string = address_string
                address_object_list.append(address)   
    return address_object_list


def read_coordinate_input(infile): 
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        __check_coordinate_input(csvReader)
        address_object_list = []
        for row in csvReader:
            latitude = row[0]
            longitude = row[1]
            #TODO:change condition based on actual input
            if latitude and longitude:
                address = Address()
                address.latitude = latitude
                address.longitude = longitude  
                address_object_list.append(address)
    return address_object_list


# helpers to ensure correct format of input 
def __check_address_input(csvReader):
    try:
        csv_headers = csvReader.__next__() 
        assert len(csv_headers) == 1, \
               "input must consist of address csv with one column called 'address' "
    except StopIteration:
        print("\n Error: ensure input file not empty \n")
        raise 
    except AssertionError:
        raise


def __check_coordinate_input(csvReader):
    try:
        csv_headers = csvReader.__next__() 
        assert len(csv_headers) == 2, \
               "input must be csv with two columns of coordinates: 'latitude', 'longitude' "
    except StopIteration:
        print("\n Error: ensure input file not empty \n")
        raise 
    except AssertionError:
        raise


############ Functions to write to csv output files ############# 
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


def write_reverse_geocode_csv_output(processed_address_list, outfile):
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        __write_reverse_geocode_header(csvWriter)
        for address in processed_address_list:
            __write_reverse_geocode_data(csvWriter, address)


# helpers for csv writing functions 
def __write_forward_geocode_header(csvWriter):
    csvWriter.writerow(['address', 'latitude', 'longitude'])

def __write_forward_geocode_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([f'{str(address.input_string)}',
                            address.latitude,
                            address.longitude ])
    else: 
        csvWriter.writerow([f'{str(address.input_string)}',
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING])


def __write_validation_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])

def __write_validation_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([f'{str(address.input_string)}',
                            OUTPUT_CSV_TRUE,
                            f'{str(address.line_1)}, {str(address.line_2)}'])
    else: 
        csvWriter.writerow([f'{str(address.input_string)}',
                            OUTPUT_CSV_FALSE,
                            OUTPUT_CSV_NULL_STRING])


def __write_general_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', \
                        'corrected_address', 'latitude', 'longitude'])

def __write_general_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([f'{str(address.input_string)}',
                            OUTPUT_CSV_TRUE,
                            f'{str(address.line_1)}, {str(address.line_2)}',
                            address.latitude,
                            address.longitude ])
    else: 
        csvWriter.writerow([f'{str(address.input_string)}',
                            OUTPUT_CSV_FALSE,
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING])


def __write_reverse_geocode_header(csvWriter):
    csvWriter.writerow(['latitude', 'longitude', 'address'])

def __write_reverse_geocode_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([address.latitude,
                            address.longitude,
                            f'{str(address.line_1)}'])
    else: 
        csvWriter.writerow([address.latitude,
                            address.longitude,
                            OUTPUT_CSV_NULL_STRING])
                         