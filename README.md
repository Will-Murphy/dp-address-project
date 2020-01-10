#  DP-Address-Project 
### this project was done for Decision Point Healthcare Solutions : https://decisionpointhealth.com ###

## Sample usage :
python3 provider_address.py provider_address.py --config [CONFIG] --infile [INFILE] --outfile
                           [OUTFILE] [--geocode [GEOCODE]] [--geoval [GEOVAL]]

### For Address Validation and Standardization ONLY ###
python3 provider_address.py --config ../config.cfg --infile '../npi-sample-data/npi_sample_batch.csv' --outfile 'validation_sample_output.csv' 

### For Address Geocoding Only ###
williammurphy$ python3 provider_address.py --config ../config.cfg --infile '../npi-sample-data/npi_sample_batch.csv' --outfile 'geocoding_sample_output.csv' --geocode True

### For Address Validation and Standardization and Address Geocoding ###
python3 provider_address.py --config ../config.cfg --infile '../npi-sample-data/npi_sample_batch.csv' --outfile 'geocoding_and_validation_sample_out.csv' --geoval True
    
## Notes :
 - Third Party GeoCoding and Address Valdiation Service: Smarty Streets 
  - Will probably desgin such that run batch can decide about stream or batch input and handle it
    nearly identically

### SMARTY STREET specific notes ###: 
 - MAX_BATCH_SIZE = 100 lookups/request
 - "freeform" input address is saved in the smarty streets 'Lookup' object in the 'street' attribute  
 -  Later use potentially address opensource lib for problem "freeform" inputs, or altogether

 