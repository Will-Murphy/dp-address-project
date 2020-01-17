"""
Input/output utilities to help address service class read and produce csv files. 
Responsible for creation of address objects from input. 
"""

import csv

from models.address import Address

#TODO: make these constants potential program inputs for batch option in main
OUTPUT_CSV_NULL_STRING = ""
OUTPUT_CSV_FALSE_STRING = "FALSE"
OUTPUT_CSV_TRUE_STRING = "TRUE"


############ Functions to read from csv input files ############# 
def read_address_input(infile):
    """Read input address csv into list of address objects."""
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        __check_address_input(csvReader)
        address_object_list = []
        for row in csvReader:
            address_string = str(row[0])
            if address_string:
                address = Address()
                address.input_string = address_string
                address_object_list.append(address)   
    return address_object_list


def read_coordinate_input(infile): 
    """Read input coordinate csv into list of address objects."""
    with open (infile, newline = '') as csv_address_infile:
        csvReader = csv.reader(csv_address_infile, delimiter = ',')
        __check_coordinate_input(csvReader)
        address_object_list = []
        for row in csvReader:
            latitude = str(row[0])
            longitude = str(row[1])
            if latitude and longitude:
                address = Address()
                address.latitude = latitude
                address.longitude = longitude  
                address_object_list.append(address)
    return address_object_list


def __check_address_input(csvReader):
    """Check address formating of input address csv file."""
    try:
        csv_headers = next(csvReader) 
        assert len(csv_headers) == 1, \
               'input must consist of address csv with one column called "address"'
    except StopIteration:
        print('\n Error: ensure input file not empty \n')
        raise 
    except AssertionError:
        raise


def __check_coordinate_input(csvReader):
    """Check address formating of input coordinate csv file."""
    try:
        csv_headers = next(csvReader)
        assert len(csv_headers) == 2, \
            'input must be csv with two columns of coordinates: "latitude", "longitude"'
    except StopIteration:
        print('\n Error: ensure input file not empty \n')
        raise 
    except AssertionError:
        raise


############ Functions to write to csv output files ############# 
def write_forward_geocode_csv_output(processed_address_list, outfile):
    """Main fn for writing forward geocode csv output using helper fns"""
    __write_output_csv_helper(processed_address_list, 
                              outfile, 
                              __write_forward_geocode_header, 
                              __write_forward_geocode_data)

def write_validation_csv_output(processed_address_list, outfile): 
    """Main fn for writing address validation csv output using helper fns"""
    __write_output_csv_helper(processed_address_list, 
                              outfile, 
                              __write_validation_header, 
                              __write_validation_data)


def write_general_csv_output(processed_address_list, outfile): 
    """Main fn for writing general csv output using helper fns"""
    __write_output_csv_helper(processed_address_list, 
                              outfile, 
                              __write_general_header, 
                              __write_general_data)


def write_reverse_geocode_csv_output(processed_address_list, outfile):
    """Main func for writing reverse geocode csv output using helper fns"""
    __write_output_csv_helper(processed_address_list, 
                              outfile, 
                              __write_reverse_geocode_header, 
                              __write_reverse_geocode_data)


# helpers for csv writing functions 
def __write_output_csv_helper(processed_address_list, outfile 
                              ,header_writer_func, data_writer_func):
    """
    helper using csv writer class with header and data writer helpers
    to do the work of writing csv output.
    """
    with open (outfile, 'w', newline = '') as csv_address_outfile: 
        csvWriter = csv.writer(csv_address_outfile, delimiter = ',')
        header_writer_func(csvWriter)
        for address in processed_address_list:
            data_writer_func(csvWriter,address)


def __write_forward_geocode_header(csvWriter):
    csvWriter.writerow(['address', 'latitude', 'longitude'])

def __write_forward_geocode_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([address.input_string,
                            address.latitude,
                            address.longitude])
    else: 
        csvWriter.writerow([address.input_string,
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING])


def __write_validation_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', 'corrected_address'])

def __write_validation_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([address.input_string,
                            OUTPUT_CSV_TRUE_STRING,
                            address.get_standardized_string()])
    else: 
        csvWriter.writerow([address.input_string,
                            OUTPUT_CSV_FALSE_STRING,
                            OUTPUT_CSV_NULL_STRING])


def __write_general_header(csvWriter): 
    csvWriter.writerow(['address', 'is_valid', \
                        'corrected_address', 'latitude', 'longitude'])

def __write_general_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([address.input_string,
                            OUTPUT_CSV_TRUE_STRING,
                            address.get_standardized_string(),
                            address.latitude,
                            address.longitude ])
    else: 
        csvWriter.writerow([address.input_string,
                            OUTPUT_CSV_FALSE_STRING,
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING,
                            OUTPUT_CSV_NULL_STRING])


def __write_reverse_geocode_header(csvWriter):
    csvWriter.writerow(['latitude', 'longitude', 'address'])

def __write_reverse_geocode_data(csvWriter, address):
    if address.is_valid:
        csvWriter.writerow([address.latitude,
                            address.longitude,
                            address.get_standardized_string()])
    else: 
        csvWriter.writerow([address.latitude,
                            address.longitude,
                            OUTPUT_CSV_NULL_STRING])
                         