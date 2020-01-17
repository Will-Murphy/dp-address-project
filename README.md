#  DP-Address-Project 
*This project was done for Decision Point Healthcare Solutions:* https://decisionpointhealth.com 

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

## Details on Third Party Use and Program Behavior:

### Validation with Smarty Streets: 

#### Important Details:
For incorrect/malformatted addresses for which Smarty Streets is still able to find a match, as well as for ones
which are already valid without changes, the API will return a list of candidates with standardized address 
as follows (note this can also be broken into its further components):

   ```
   [address line 1 (i.e. number - street - specific details)], [address line 2 (i.e. city - state - zip+4)] 
   ```
This program chooses the one in which Smarty's API is most confident, as it rates each candidates confidence level. If it can't 
find confident matches, it returns none, meaning it believes the address to be invalid. In both cases, smarty streets also returns an 
analysis of the input address, which can be further analyzed but is not in this implementation. 

***NOTE:*** Smarty Streets is very good at only returning addresses if they are valid. However, There are a non-neglible number 
of seemingly valid addresses that are marked as Invalid by smarty streets (seems around %2-5). For these it seems that 
SMARTY API has trouble parsing out the address components for particularly long( with long building names) or specifically 
formatted addresses. Potential solutions included in next steps section. 
Here are a couple example problem inputs with no smarty candidates returned but which are valid. 

- **5453 HIGHWAY 2, PRIEST RIVER ID 83856**
- **8390 HIGHWAY 51 NORTH 101, MILLINGTON TN 38053**
- **LIFESPAN THERAPY 118 MEDICAL DRIVE, CARMEL IN 46032**
- **HILLTOWN COMMUNITY HEALTH CENTER - SCHOOL-BASED PROGRAM 12 LITTLEVILLE ROAD, HUNTINGTON MA 01050**
- **1401 N WINDING BROOK LOOP, PALMER AK 99645**

#### Batch Behavior:
If smarty streets can find a candidate, this program returns **"TRUE"** in the **is_valid** column of output
and returns the above standardized address of the top candidate in the **corrected_address** column. 
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
Given an coordinate set, Open Cage (and nearly all reverse geocodoers) will try to match the the coordinates to the nearest, most specific address down to the street number. 
It cant find a specific location, it will return the street, and then the city etc... 
If there is no match it will return nothing. 

#### Batch Behavior: 
Given an lat, long batch, the most specific address found will be output to the **address** column, otherwise returns the empty string **""**. 

#### Stream Behavior: 
Given input coordinate string, returns string the most specific address found, string saying the input coordinare string is invalid is returned. 

            
## Next Steps: 
 
### Solve False Invalid Address Outputs (address marked invalid when its really valid): ### 
(see details in validation with smarty streets section for more info on why this needed )
- **Multi-Service Script Composition Solution:**
    - Add a parameter to **batch_main.py** called --invalid_list that 
               when given a file name, produces a csv of input addresses found to be
               invalid and their index in the original input csv.
     - Compose calls to this program to run address validation again but now on 
               this narrowed down invalid list and with a different service (open cage or other), 
               in order to double check problem inputs. If they are found to be wrongly 
               marked invalid, update original input csv. 
- **Address Parsing Script Compostion Solution:**
      - Add a parameter to **batch_main.py** called --invalid_list that 
               when given a file name, produces a csv of input addresses found to be
               invalid and their index in the original input csv file.
      - Use open source address parser to break invalid addresses into components
               and feed that input back into smarty streets ( so it can validate more 
               effectively, and some of these address parsers are up to 99% accurate in breaking
               address into compoenents) .If they are found to be wrongly marked invalid, update 
               original input csv. 
               (https://github.com/openvenues/libpostal)
- **Try Another Service: (hopefully as simple as creating another address class)**
      - Map Based Service: Smarty Validates addresses based on the USPS database of deliverable addresses, 
              whereas google uses mapping data to place an address string as accurately as it can on a map. 
              Once google (or other services) do this it can give you directions there accurately, 
              but it doesn't really care if the address itself is valid, as long as it maps correctly 
              location-wise.Still, it seems to find addresses better through this method, 
              and potentially could turn out to be a better fit for DP's use cases, even though it is not strictly
              validating. 
      - Another Validation service: There are multiple other enterprise level validation services using 
              the USPS database, but I could find no indication that they are any better than smarty, 
              and most they don't include trials or pricing so it was hard to compare - but still might 
              be worth looking into. 

### Turn into flask API: 

- Make a flask API that depending on request type and params will call this program so that it correctly 
returns the service the user is looking for, and allow for composition of script calls as mentioned in 
the **Solve False Invalid Address Outputs** section above. 

- This will allow this program to be exposed to multiple  end users and make it more dynamic 

### Testing: 
- **Integration testing:** check that different needs and use cases are adaqautely provided by this service
                       both for data and product teams. 
- **Unit Testing:** Most of the functions will check for invalid input and but all cases on ever function 
                have not been tested for. 



   



 