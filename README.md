#  DP-Address-Project 
this project was done for Decision Point Healthcare Solutions : https://decisionpointhealth.com 

## Sample usage :

### For Address Validation and Forward Geocoding ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/forward_geocoding_and_validation_output.csv' --options 0
 
### For Forward Address Geocoding Only ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/forward_geocoding_output.csv' --options 1

### For Address Validation and Standardization ONLY ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/validation_output.csv' --options 2

### For Reverse Address Geocoding Only ###
python3 main.py --config ../config.cfg --infile '../sample-input-output/sample_coordinate_input.csv' --outfile '../sample-input-output/reverse_geocoding_output.csv' --options 3


## Sample input/output files: 
see sample-input-output directory 


## Notes :
 - Third Party Forward GeoCoding and Address Valdiation Service: Smarty Streets 
 - Third Party Reverse Geocoding Service: Open cage
 - Will probably desgin such that run batch can decide about stream or batch input and handle it
    nearly identically

### SMARTY STREET specific notes ###: 
 - MAX_BATCH_SIZE = 100 lookups/request
 - "freeform" input address is saved in the smarty streets 'Lookup' object in the 'street' attribute  
 -  Later use potentially address opensource lib for problem "freeform" inputs, or altogether

 