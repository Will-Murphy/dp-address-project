#  DP-Address-Project 
this project was done for Decision Point Healthcare Solutions : https://decisionpointhealth.com 

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

## Notes :
 - Third Party Forward GeoCoding and Address Valdiation Service: Smarty Streets 
 - Third Party Reverse Geocoding Service: Open cage
 These services are interchangable with other services so long as they fit 
 the address service interface enforced by the the address service class
