#  DP-Address-Project 
*This project was done for Decision Point Healthcare Solutions:* https://decisionpointhealth.com 
*by Will Murphy Jan 2020.* 

This project handles stream/batch of address data, either in coordinate or string form, and provides an interface to connect to third party 
services in order to process that data for validation, standardization and geocoding. It then produces processed output data which matches the form of the input. 

## Notes: 
   **Third Party Services Used**
   - Third Party Forward Geocoding and Address Valdiation Service: SmartyStreets (https://smartystreets.com) 
   - Third Party Reverse Geocoding Service (though forward geocoding implemented for use here as well): OpenCageData (https://opencagedata.com)

   **Implementation Details**
   - These third party services are interchangable with other services so long as their implementations (**src/services/...**) reside
      in classes that inherit from the *AddressService* abstract class (**src/models/address_service.py**) e.g. 
      *SmartyAddressService* does all but reverse geocoding, which *OpenCageAddressService* handles, and both inherit 
      from *AddressService*
   - All data processing done inside these third party implementations of *AddressService* classes is done in terms of the *Address* 
     objects (**src/models/Address.py**)
   - All input/output is handled by utililites(**src/utilities/..**)
   - Designed so you can run addresses through multiple rounds of processing by composing functionality from two different services or 
     within the same service.
     (see **src/main_batch.py** & **src/main_batch.py** )
 
## Setup and Requirements:
- python 3.6 or higher required 

- Smarty Streets official python sdk: ```pip3 install smartystreets_python_sdk```
  - more info: (https://github.com/smartystreets/smartystreets-python-sdk)

- OpenCage recommended python sdk: ```pip3 install opencage```
  - more info: (https://opencagedata.com/tutorials/geocode-in-python)

- Go to Services website for API keys and fill them in the **src/sample_config.cfg** file 
    - For Smarty Streets : 
      1. go to https://smartystreets.com/pricing and choose the free
         option with 250 lookups per month (wow!). 
      2. Make an account (no account verification needed)
      3. Go to the account management dashboard and API keys section to get 
         your Auth ID and Auth Token 
      4. Fill in your auth_id and auth_token (under those names) in the **sample_config.cfg**
         file in under the smarty streets header
    - For Open Cage: 
      1. go to https://opencagedata.com/pricing and choose the free option limited to 
         2,500 req/day and 1 req/sec  
      2. Make an account and verfiy by email 
      3. Get your API key by email after having an acct. 
      4. put it in the auth_key section of **sample_config.cfg** under the 
         open cage header 
      
## Program Usage: 

first cd into src directory: **dp-provider-address/src/* 

#### For Batch CSV Input: 
Running the following example commands should work as is if set up above is completed correctly,
resulting in sample output to '/dp-provider-address/sample-input-output/out.csv' based on the 
sample input file and options selected. **program arguments**:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--infile```  input csv batch file (see sample-input-output dir)
-  ```--outfile``` output csv batch file (see sample-input-output dir)
-  ```--options``` options for processing input data (see below)

      
   ##### Batch Address Validation and Forward Geocoding: option 0 #####
   ```  
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 0
   ```
   ##### Batch Address Validation Only: option 1 #####
   ```
   python3 main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 1
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
for given input. **program arguments**:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--input```  input string containing address or comma separated coordinates
-  ```--options``` options for processing input (see below)
  
   ##### Stream Address Validation and Forward Geocoding: option 0 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 0
   ```
   ##### Stream Address Validation Only: option 1 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 1
   ```
   ##### Stream Address Forward Geocoding Only: option 2 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 2
   ```
   ##### Stream Address Reverse Geocoding Only: option 3 #####
   ```
   python3 main_stream.py --config ../sample_config.cfg --input="42.3574, -71.05477"  --options 3
   ```

## Sample Input/Output Files For Batch Processing: 
see **sample-input-output** directory for sample csv files

## Detils on Third Party Specific Program Behaviour:

###Validation with Smarty Streets: 
####details:
For incorrect/malformatted addresses for which Smarty Streets can find a match, as well as for ones
which are already valid without changes, it will return it a list of candidates with standardized address 
as follows (note this can also be broken into its further components):

      address line 1 (i.e. number - street - specific details)], [address line 2 (i.e. city - state - zip+4)]

This program chooses the one in which it is most confident. If it can find none with confidence, it returns none, meaning it
believes the address to be invalid. Smarty streets also returns an analysis of the input address which can be further analyzed 
but is not in this program. 

see **sample-input-out/sample_invalid_addresses** as some addresses that are valid cannot be found by smarty. 
####batch:
This program returns **"TRUE"** in the **is_valid** column of output
and returns the above standardized address in the **corrected_address** column if smarty streets
can find one . This happens *EVEN IF THE INPUT ADDRESS IS ALREADY CORRECT*: Otherwise **is_valid** 
is **False** and **corrected_address** is the empty string. 
###stream: 
If an address string is found to be valid, the same type of standardized address as is in **batch** above is returned 
*EVEN IF THE INPUT ADDRESS IS ALREADY CORRECT*. Otherwise a string saying the input address string is invalid is returned. 

###Forward Geocoding: 
####details: 
Smarty Streets Validates and Forward geocodes in one step, geocoding only after address has been validated. 
####batch:
After address is validated, populates **latitude**, **longitude** csv column with closest coordinates tha could be found to input address. If address could not 
be validated or coordinates not found, those columns will contain the empty string **""**
####stream: 
After input address string is validated, a string containing coordinates returned. Otherwise a 
string saying the input address string is invalid is returned. 

### Reverse Geocoding:
####details:
Given an coordinate set, Open Cage (and nearly all reverse geocodoers) will try to match the the coordinates to the nearest, most specific address down to the street number. 
It cant find a specific location, it will return the street, and then the city etc... 
If there is no match it will return nothing. 
####batch: 
Given an lat, long batch, the most specific address found will be output to the **address** column, otherwise returns the empty string **""**. 
####stream: 
Given input coordinate string, returns string the most specific address found, string saying the input coordinare string is invalid is returned. 

            
## Next Steps: 

####test/test plans: 
A lot of input string 

smarty invalid issues 

compose invalid addresses from smarty with open cage to ensure they are really invalid

turn into flask api 

add option to return invalid address list

third party address parsing (99% correct and free) 
   



 