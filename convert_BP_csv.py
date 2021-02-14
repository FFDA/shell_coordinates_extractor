#! /usr/bin/python3

## This script will convert 'company' provided BP list. User has to export provded xlsx file to csv.

from os import listdir
from sys import exit
import csv
from ASCII_Translator import ascii_dict

csv_list = []

for item in listdir():
    if item[-4:].lower() == ".csv":
        csv_list.append(item)

if len(csv_list) != 0:
    print("Choose a file. Choose 'company' provided BP list that has been exported to csv.")
    print("Type a number:")
    for item in range(len(csv_list)):
        print(str(item) + ". " + csv_list[item])
    file_to_convert = input()

    if int(file_to_convert) not in range(len(csv_list)):
        print("You chose poorly.")
        exit()
else:
    print("I counldn't find any .csv files in directory.")
    print("You have to place them in the same directory you launch this script.")

convert_to = open("Berstchi_BP"+ "_mymaps" + ".csv", mode="w")
convert_to_writer = csv.writer(convert_to)
convert_to_writer.writerow(["Latitude", "Longitude", "Name", "Address", "City", "Postcode"])

with open(csv_list[int(file_to_convert)], mode="r") as convert_from:
    convert_from_reader = csv.reader(convert_from)

    for line in convert_from_reader:
        new_line = []
        new_line.append(line[9].translate(ascii_dict)) # Latitude
        new_line.append(line[8].translate(ascii_dict)) # Longitude

        ## Comment out these 4 line for TomTom CSV
        ## This part creates CSV file for google's mymaps
        new_line.append(line[2].translate(ascii_dict)) # Name
        new_line.append(line[5].translate(ascii_dict) + " " + line[6].translate(ascii_dict)) # Address
        new_line.append(line[4].translate(ascii_dict)) # City
        new_line.append(line[3].translate(ascii_dict)) # Postcode
        ##

        ## This line uncomment if you want to make csv for TomTom. The four above has to be commented out.
        # new_line.append(line[2].translate(ascii_dict) + "; " + line[5].translate(ascii_dict) + " " + line[6].translate(ascii_dict) + "; " + line[4].translate(ascii_dict) + "; " + line[3].translate(ascii_dict))
        ##
        
        convert_to_writer.writerow(new_line)


convert_to.close()