#  DP-Address-Project 
This project was done for Decision Point Healthcare Solutions: https://decisionpointhealth.com 

This project handles stream/batch of address data, either in coordinate or string form, and provides an interface to connect to third party 
services and to process that data for validation, standardization and geocoding. It then produces processed output data which matches the form of the input. 

#### Notes: ####
   **Third Party Services**
   - Third Party Forward GeoCoding and Address Valdiation Service: SmartyStreets (https://smartystreets.com) 
   - Third Party Reverse Geocoding Service: OpenCageData (https://opencagedata.com)

   **Implementation details**
   - These third party services are interchangable with other services so long as their implementations reside
      in classes that inherit from the *AddressService* abstract class ( see **src/models/address_service.py** ) e.g. 
      *SmartStreetsAddressService* does all but reverse geocoding, which *OpenCageAddressService* handles, and both inherit 
      from *AddressService*
   - All data processing done inside these implementatioms of *AddressService* classes is done terms of the *Address* objects. 
   - All input/output processing is handled by utility classes (**utilities/stream_io.py** or **utilities/batch_io.py**)
   


## Setup and Usage:

### Setup and Requirements
- python 3.6 or higher required 

- Smarty Streets official sdk: ```pip3 install smartystreets_python_sdk```
  - more info: (https://github.com/smartystreets/smartystreets-python-sdk)

- OpenCage official sdk: ```pip3 install opencage```
  - more info: (https://opencagedata.com/tutorials/geocode-in-python)

- Go to Services website for API keys and fill them in the sample_config.cfg file 
    - For Smarty Streets : 
      1. go to https://smartystreets.com/pricing and choose the free
         option with 250 lookups per month (wow!). 
      2. Make an account (no account verification needed)
      3. Go to the account management dashboard and API keys section to get 
         your Auth ID and Auth Token 
      4. Fill in your auth_id and auth_token (under those names) in the sample_config.cfg 
         file in under the smarty streets header
    - For Open Cage: 
      1. go to https://opencagedata.com/pricing and choose the free option limited to 
         2,500 req/day and 1 req/sec  
      2. Make an account and verfiy by email 
      3. Get your API key by email after having an acct. 
      4. put it in the auth_key section of sample_config.cfg under the 
         open cage header 
      


### Program Usage
first cd into directory: **dp-provider-address/src/** 

   
#### For Batch CSV Input: 
Running the following example commands should work as is if set up above is completed correctly,
resulting in sample output to '/dp-provider-address/sample-input-output/out.csv' based on the 
sample input file and options selected. **program arguments**:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--infile```  input csv batch file (see sample_inputs)
-  ```--outfile``` output csv batch file to direct output to
-  ```--options``` options for processing input data (see below)

      
   ##### Batch Address Validation and Forward Geocoding: option 0 #####
   ```  
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 0
   ```
   ##### Batch Address Validation Only: option 1 #####
   ```
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../ sample-input-output/out' --options 1
   ```
   ##### Batch Forward Geocoding Only: option 2 #####
   ```
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 2
   ```
   ##### Batch Reverse Geocoding: option 3 #####
   ```
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_coordinate_input.csv' --outfile '../ sample-input-output/out.csv' --options 3
   ```

#### For Single String Stream Input: 
Running the following example commands should work as is and will both return and print the string results 
for given input. **program arguments**:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--input```  input string containing address or comma separated coordinates
-  ```--options``` options for processing input (see below)
  
   ##### Stream Address Validation and Forward Geocoding: option 0 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input "2 Oliver St, Boston MA"  --options 0
   ```
   ##### Stream Address Validation Only: option 1 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input "2 Oliver St, Boston MA"  --options 1
   ```
   ##### Stream Address Forward Geocoding Only: option 2 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input "2 Oliver St, Boston MA"  --options 2
   ```
   ##### Stream Address Reverse Geocoding Only: option 3 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input  "42.3574, -71.05477"  --options 3
   ```

## Sample input/output files for batch processing: 
see **sample-input-output** directory 


 