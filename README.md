#  DP-Address-Project 
This project was done for Decision Point Healthcare Solutions: https://decisionpointhealth.com 

This project handles stream/batch of address data, either in coordinate or string form, and provides an interface to connect to third party 
services to process that data for validation, standardization and geocoding. It then produces processed output data which matching the form of the input. 

### Notes :
 - Third Party Forward GeoCoding and Address Valdiation Service: Smarty Streets 
 - Third Party Reverse Geocoding Service: Open cage geocoding 
 - These third party services are interchangable with other services so long as they adhere to sturcture 
   defined by address service abstract class ( see address_service.py ) e.g. 
   smarty streets does all but reverse geocoding, which opencage handles. 


## Setup and Usage:

### Setup 
- python 3.6 or higher required 

- Dependencies from third party services 
    Smarty Streets: ```pip3 install smartystreets_python_sdk```
    more info: (https://github.com/smartystreets/smartystreets-python-sdk)

    OpenCage: ```pip3 install opencage```
    more info: (https://opencagedata.com/tutorials/geocode-in-python)

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
sample input file and options selected. arguments:
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
  python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out' --options 1
  ```
  ##### Batch Forward Geocoding Only: option 2 #####
  ```
  python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 2
  ```
  ##### Batch Reverse Geocoding: option 3 #####
  ```
  python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_coordinate_input.csv' --outfile '../sample-input-output/out.csv' --options 3
  ```

#### For Single String Stream Input: 
Running the following example commands should work as is and will both return and print the string results 
for the given input. arguments:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--infile```  input string 
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

## Sample input/output files: 
see sample-input-output directory 


 