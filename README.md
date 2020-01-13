#  DP-Address-Project 
This project was done for Decision Point Healthcare Solutions: https://decisionpointhealth.com 

### Notes :
 - Third Party Forward GeoCoding and Address Valdiation Service: Smarty Streets 
 - Third Party Reverse Geocoding Service: Open cage geocoding 
 - These third party services are interchangable with other services so long as they adhere to sturcture 
   defined by address service abstract class ( see address_service.py )

## Sample usage :

### For Address Validation and Forward Geocoding ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/forward_geocoding_and_validation_output.csv' --options 0
 
### For Forward Address Geocoding Only ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/forward_geocoding_output.csv' --options 1

### For Address Validation Only ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/validation_output.csv' --options 2

### For Reverse Address Geocoding Only ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_coordinate_input.csv' --outfile '../sample-input-output/reverse_geocoding_output.csv' --options 3


## Sample input/output files: 
see sample-input-output directory 

## Dependencies/ Setup 
 External depencies needed are for the third party python sdk's used in the 
 service specific implmementation of address classes
 - Smarty streets: pip3 install smartystreets_python_sdk (https://github.com/smartystreets/smartystreets-python-sdk)
 - Open Cage: pip3 install opencage (https://opencagedata.com/tutorials/geocode-in-python)
