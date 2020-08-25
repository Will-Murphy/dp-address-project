#  DP-Address-Project 
*This project was done for Decision Point Healthcare Solutions:* https://decisionpointhealth.com 

Microservice for proccessing stream/batch address data for validation, standardization and two-way geocoding. Provides an internal interface for connecting too and implementing third party services to process address data and produce desired output data. 

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
   - All input/output of address objects is handled by utililites(**src/utilities/..**)
   - Designed to allow for running address data through multiple rounds of processing by composing functionality from two different services    or within the same service (see **src/main_batch.py** & **src/main_batch.py** )
   - Smarty Streets official python sdk was used to implement *SmartyAddressService* : (https://github.com/smartystreets/smartystreets-python-sdk)
   - OpenCage recommended python sdk was used to implemement *OpenCageAddressService*: (https://opencagedata.com/tutorials/geocode-in-python)
 
## Setup and Requirements:
1. python 3.6 or higher required 

2. External Python Depenedencies using ```pipenv```
  1. cd src directory: **dp-provider-address/src/**
  2. if your don't already have it download pipenv: ```pip install pipenv```
  3. run ```pipenv install && pipenv shell```
  
3. Go to Services website for API keys and fill them in the **src/sample_config.cfg** file 
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

Ensure you are in **dp-provider-address/src/** with pipenv shell activated and installed ( setup step 2)

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
   python main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 0
   ```
   ##### Batch Address Validation Only: option 1 #####
   ```
   python main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 1
   ```
   ##### Batch Forward Geocoding Only: option 2 #####
   ```
   python main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_address_input.csv' --outfile '../sample-input-output/out.csv' --options 2
   ```
   ##### Batch Reverse Geocoding: option 3 #####
   ```
   python main_batch.py --config ../sample_config.cfg --infile '../sample-input-output/sample_coordinate_input.csv' --outfile '../sample-input-output/out.csv' --options 3
   ```

#### For Single String Stream Input: 
Running the following example commands should work as is and will both return and print the string results 
for given input. **program arguments**:
-  ```--config```  configuration file (see sample_config.cfg)
-  ```--input```  input string containing address or comma separated coordinates
-  ```--options``` options for processing input (see below)
  
   ##### Stream Address Validation and Forward Geocoding: option 0 #####
   ```
   python main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 0
   ```
   ##### Stream Address Validation Only: option 1 #####
   ```
   python main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 1
   ```
   ##### Stream Address Forward Geocoding Only: option 2 #####
   ```
   python main_stream.py --config ../sample_config.cfg --input="2 Oliver St, Boston MA"  --options 2
   ```
   ##### Stream Address Reverse Geocoding Only: option 3 #####
   ```
   python main_stream.py --config ../sample_config.cfg --input="42.3574, -71.05477"  --options 3
   ```

## Sample Input/Output Files For Batch Processing: 
see **sample-input-output** directory for sample csv files

## Details on Third Party Use and Program Behavior:

### Validation with Smarty Streets: 

#### Important Details:

If Smarty Streets finds a valid match on an address string, the API will return a list of candidates with address formatted data,
components, metadata, and analysis. For incorrect/malformatted addresses for which Smarty Streets is still able to find a match, as well as for ones which are already valid without changes, this program grabs the formatted address delivery line 1 and line 2 of the top candidate match that the API can find to provide a validated, standardized address as follows. 

   ```
   [address line 1 (i.e. number - street - specific details)], [address line 2 (i.e. city - state - zip+4)] 
   ```
The lookup parameters by default are set to return a candidate only if smarty streets is very confident in its match. This program chooses strictly the candidate in which Smarty's API is most confident. If it can't find confident matches, it returns no candiates, meaning the address is invalid. In both cases though, the API also returns an analysis of the input address, and an option to allow for less stringent validation, which could be helpful moving forward..

***NOTE:*** Smarty Streets is very good at only returning addresses if they are valid. However, There are a non-neglible number 
of seemingly valid addresses that are marked as Invalid by smarty streets (seems around %2-3). For these it seems that 
SMARTY API has trouble parsing out the address components for particularly long( with long building names) or specifically 
formatted addresses, and is not confident in its matches.
Below are a couple example problem inputs with no smarty candidates returned but which are valid. 

- **5453 HIGHWAY 2, PRIEST RIVER ID 83856**
- **8390 HIGHWAY 51 NORTH 101, MILLINGTON TN 38053**
- **LIFESPAN THERAPY 118 MEDICAL DRIVE, CARMEL IN 46032**
- **HILLTOWN COMMUNITY HEALTH CENTER - SCHOOL-BASED PROGRAM 12 LITTLEVILLE ROAD, HUNTINGTON MA 01050**
- **1401 N WINDING BROOK LOOP, PALMER AK 99645**

#### Batch Behavior:
If smarty streets is able to find a candidate, this program returns **"TRUE"** in the **is_valid** column of output and returns the above standardized address of the top candidate in the **corrected_address** column. 
This happens *EVEN IF THE INPUT ADDRESS IS ALREADY CORRECT*. Otherwise **is_valid** 
is **"FALSE** and **corrected_address** is the empty string. 

#### Stream Behavior: 
If an address string is found to be valid, the same type of standardized address as is in **batch** above is returned 
*EVEN IF THE INPUT ADDRESS IS ALREADY CORRECT*. Otherwise a string saying the input address string is invalid is returned. 

### Forward Geocoding with Smarty Streets:

#### Important Details:
Smarty Streets Validates and Forward geocodes in one step, geocoding only after address has been validated. 

#### Batch Behavior:
After address is validated, populates **latitude**, **longitude** csv column with closest coordinates tha could be found to input address. If address could not 
be validated or coordinates not found, those columns will contain the empty string.

#### Stream Behavior: 
After input address string is validated, a string containing coordinates returned. Otherwise a 
string saying the input address string is invalid is returned. 

### Reverse Geocoding with Open Cage: ###

#### Important Details:
Given an coordinate set, Open Cage (and nearly all reverse geocodoers) will try to match the the coordinates to the nearest, most specific address down to the street number so address formatting may vary.
For example, If it can't find a specific location, it will return the street, and then the city etc... 
If there is no match it will return nothing. 

#### Batch Behavior: 
Given an lat, long batch, the most specific address found will be output to the **address** column, otherwise returns the empty string **""**. 

#### Stream Behavior: 
Given input coordinate string, returns string the most specific address found, string saying the input coordinare string is invalid is returned. 
