#! /usr/bin/python3

# This script will make a csv file that can be converted to TomTom POI file from table that was extracted from 'company' shell gastation list.
# It will use google to search for the shell website, extract all the info that is needed and add it to new file.
# If it will not be able to find a gas station it will and a message the file instead of skipping.
# Depending on how long is a post code pass -p4 or -p5 as an argument when launching program.

gas_station_list = "Shell_Czechia_2020_test.csv"

import csv
from googlesearch import search
from time import sleep
from urllib import request, response
from bs4 import BeautifulSoup
import re
from ASCII_Translator import ascii_dict
from sys import argv
from urllib import error
from random import randint

counter = 0

POI_file = open("POI_file.csv", mode="w", encoding="UTF-8", newline="\n")
POI_file_writer = csv.writer(POI_file, delimiter=",", quotechar='"')

def get_shell_website(search_term):
    ## Searched the web using google and looks for shell website in results

    search_result = search(search_term)

    for result in search_result:
        if "find.shell.com" in result:
        # If finds a match it returns it and breaks
            return result
            break
        
    return ""

def get_coordinates_from_link(soup):
    ## Gets google link with coordinates embeded in shell website, extracting coordinates using regular expresiosn
    
    # Finding all links with class "hero__directions-button". Should find one.
    coordinate_link = soup.find_all("a", class_="hero__directions-button")

    if len(coordinate_link) == 1:
    # If search in website found one link with class "hero__directions-button"
        link_with_coordinates = coordinate_link[0].get("href") # gets the link

        coordinate_search_re = re.compile("=(-*\d+\.\d+)%2C(-*\d+\.\d+)")

        coordinates = coordinate_search_re.search(link_with_coordinates)
        latitude = coordinates.group(1)
        longitude = coordinates.group(2)

        return latitude, longitude
    
    else:
    # If more or less than one link found.
        return "", coordinate_link

def print_debug_error(shell_website_address, shell_website_city, shell_website_post_code):
    ## Printing messages that will allow to debug easier. It looks better how it is printed in terminal.
    print("Shl: " + shell_website_address.lower().replace(" ", "") + "|" + shell_website_city.lower() + "|" + shell_website_post_code.lower()) # DEBUG
    print("CSV: " + address.lower().replace(" ", "") + "|" + city.lower() + "|" + post_code.lower()) # DEBUG
    print("") # DEBUG

def shorten_address_list(address_list):

    while len(address_list) != 4:
        first_list_item = address_list.pop(0)
        second_list_item = address_list.pop(0)

        joined_items = first_list_item + " " + second_list_item
        address_list.insert(0, joined_items)
    
    return address_list

def compare_web_csv_info(address_list, latitude, longitude, shell_website):
## Sanitizes addresses by removing ASCII extended characters and checks address info from CSV file against extracted from shell website.
## Writes data to POI file.
    shell_website_address, shell_website_post_code, shell_website_city, shell_website_country = address_list
    shell_website_address = shell_website_address.translate(ascii_dict) # Removing all not latin letters from address
    shell_website_city = shell_website_city.translate(ascii_dict) # Removing all not latin letters from city name
    # print("Shl: " + shell_website_address.lower().replace(" ", "") + "|" + shell_website_city.lower() + "|" + shell_website_post_code.lower()) # DEBUG
    # print("CSV: " + address.lower().replace(" ", "") + "|" + city.lower() + "|" + post_code.lower()) # DEBUG
    # print("") # DEBUG
    if city.lower().replace(" ", "") == shell_website_city.lower().replace(" ", "") and post_code == shell_website_post_code and address.lower().replace(" ", "") == shell_website_address.lower().replace(" ", ""):
        if latitude != "":
            POI_file_writer.writerow([latitude, longitude, shell_website_address + "; " + shell_website_city + "; " + shell_website_post_code + "; (" + network + ")"])
        else:
        # Found more or less than 1 link with class "hero__directions-button". Writes to file:
            POI_file_writer.writerow(["Error. Expected to find 1 google maps link with coordinates.", city, name, post_code, shell_website])
    else:
        if latitude != "":                 
        # Writing error message that should help find the problem or compare the data to.
            POI_file_writer.writerow(["Error. Could not match city, adress or post_code." , "CSV: " + city + " " + address + " " + post_code + " (" + network + ")", "Shell Website: " + shell_website_address + "; " + shell_website_city + "; " + shell_website_post_code + "; (" + network + ")", shell_website, latitude, longitude])
            print_debug_error(shell_website_address, shell_website_city, shell_website_post_code)

def parse_shell_website(shell_website, website_object, city, address, post_code, network):

    soup = BeautifulSoup(website_object, "html.parser")

    # Searching for adress in the shell website
    address_span = soup.find_all("span", class_="hero__icon-row-text")

    latitude, longitude = get_coordinates_from_link(soup) # searches for latitude and longitude using another function
    
    if len(address_span) == 1:
    # If finds one span with "hero__icon-row-text" class extracts adress to check egaints the one if file
        address_list = address_span[0].string.split(", ")
        if len(address_list) == 4:
            compare_web_csv_info(address_list, latitude, longitude, shell_website)
        elif len(address_list) > 4:
        ## If address has more than 4 arguments, tries to shorten it to make it 4 and compares them
            address = shorten_address_list(address_list)
            compare_web_csv_info(address_list, latitude, longitude, shell_website)
        else:
        ## Too few arguments in address. Still getting coordinates. Can be that it matches.
            if latitude != "":
                POI_file_writer.writerow(["Error. Could not parse the address. Too few arguments. Added Complete adress.", latitude, longitude, "CSV: " + city + " " + address + " " + post_code + " (" + network + ")", "Shell Website: " + address_span[0].string + " (" + network + ")", shell_website])
                print_debug_error(address_span[0].string, "", "")
    elif len(address_span) == 0:
        # If bs4 can't find span with "hero__icon-row-text" class. Writes to line this:
        POI_file_writer.writerow(["Error. Could not find an address to match (0).", city, name, post_code, shell_website])
    else:
        # If bs4 find more than one span with "hero__icon-row-text" class. Writes to line this:
        POI_file_writer.writerow(["Error. Could not find an address to match (>1).", city, name, post_code, shell_website])

with open(gas_station_list, mode="r") as csv_file:

    read_csv_file = csv.reader(csv_file)

    for row in read_csv_file:
        city = row[0]
        address = row[1]
        name = row[2]
        post_code = row[3]
        network = row[4]

        city = city.translate(ascii_dict)
        address = address.translate(ascii_dict)
        name = name.translate(ascii_dict)

        if "-p4" in argv:
            post_code = post_code.zfill(4)
        if "-p5" in argv:
            post_code = post_code.zfill(5)

        search_term = "find.shell.com " + address + " " + city + " " + post_code

        counter += 1
        print("Searching: " + str(counter) + ". " + address + ", " + city + ", " + post_code)

        shell_website = get_shell_website(search_term)               

        try:
            # Trying to open a website. At least one in Netherlands is missing
            website_object = request.urlopen(shell_website)
            
            if shell_website != "":
                parse_shell_website(shell_website, website_object, city, address, post_code, network)
            else:
                # print(search_term) # Trinti
                POI_file_writer.writerow(["Error. Could not find it.", city, name, post_code])
        
        except error.HTTPError:
            # If can't open a shell website.
            print("Couldn't find open " + shell_website + " ; Writting to the file. ")
            POI_file_writer.writerow(["Error. Coundn't open website.", shell_website, "CSV: " + city + " " + address + " " + post_code])

        sleep_time = randint(50, 60)
        print("Sleeping for " + str(sleep_time) + " seconds.")
        sleep(sleep_time) # For now every search query will have random 5-9 second delay just google get off my ass. They can crawl the net byt when I do it for less than 200 time in 5 minutes it's a crime.


POI_file.close()
