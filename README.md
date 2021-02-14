# Shell Coordinates Extractor
This mix of scripts automates extracting from coordinates from find.shell.com website. This uses google to search for shell station in find.shell.com website. All shell station that user wants to find has to be provided using CSV file, that has to be formatted in specific way.

# Files
There are multiple scripts in this folder. Bellow are (hopefully) useful information about everyone one of them.

## shell_coordinates_extractor.py
This is main script. It makes CSV file that can be converted to TomTom (or any other) POI file suing gpsbabel. It takes another CSV file as input that can be changed on line #8. That file has to have one shell gas station per line. I was using file that has: post code, address, city name, gas station name. **f you do not have this data available exactly how it will be provided in find.shell.com website this script will not work for you.** This script file can be launch with additional options -4p or -5p. That depends for what country one tries to find a gas stations. Some countries has post codes with 4 (-p4) or 5 (-p5) symbols. These are not always needed, but for more precises matches please pass this parameter.

This script will find a gas station using google and get the data from find.shell.com website (including coordinates). Will try to match information fetch from the website to provided by the user using CSV file. If it matches date will be written to the file. If not error message will be written to the file with information that will help to debug the problem or even manually compare data.

**Google searches have a random 50 to 60 seconds pause between them because google might ban IP. User can change that on line #171**

At the end POI_file.csv will be created that will have all the information ready to be used.

## ASCII
There are four files that has ASCII in file name. They all were made for one purpose to convert non ASCII characters to ASCII for better address matching. This repo already comes with a lot of symbols in this dictionary so user might not have to do anything with these files.

#### ASCII.ods
This file has three worksheets. It was made to make a dictionary file that is used to convert non ASCII characters to ASCII that might be in user provided CSV file. First worksheet has codes and letters that represent them and explanations next to them. Second has codes, letters and corresponding codes for translations and letter next to them. Third has only codes for letter and codes for translations next to them. 

#### ASCII.csv
This file is simply created by saving third worksheet from ASCII.ods

#### make_ASCII_dict.py
Just run this file to create ASCII_Translator.py. Every time that user updates ASCII.ods and save new ASCII.csv he/she has to run this file to have an effect.

#### ASCII_Translator.py
This file contains all codes from ASCII.csv as python3 dictionary. It will be imported by shell_coordinates_extractor.py when it is run.

## shell_slovenia_coordinates_extractor.py
Because I had to provide Slovenian find.shell.com myself this file was created it is more or less exact copy of shell_coordinates_extractor.py that has some lines commented out to skip google search part.

## convert_to_mymaps_csv.py
This script convert CSV file created with shell_coordinates_extractor.py to a CSV file that can be uploaded to google's mymaps. User has just execute the script and will be prompted to choose from CSV files that are in the same directory as this script.

## convert_BP_csv.py
I had a BP gas station list for one country provided with coordinates, but not in a way that was useful for me so I created this script to convert provided file to CSV file I could use to convert with gpsbabel for TomTom or to CSV for google's mymaps.

# Requirements

- Only tested on Linux so might not work on Windows or iOS for some reason (like path formating).
- Python3
- googlesearch (pip)
- BeautifulSoup (pip)
