#! /usr/bin/python3

### Simple script to convert csv file made with shell_coordinates_extractor to csv file that would be easy to add to google's mymaps
### If user choose a file formated differently script will just crash. That's intended.

from os import listdir
from sys import exit
import csv

csv_list = []

for item in listdir():
    if item[-4:].lower() == ".csv":
        csv_list.append(item)

if len(csv_list) != 0:
    print("Choose a file. It has to be made with shell_coordinates_extractor and all errors removed or fixed, Otherwise script will crash.")
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

convert_to = open(csv_list[int(file_to_convert)][:-4] + "_mymaps" + ".csv", mode="w")
convert_to_writer = csv.writer(convert_to, quoting=csv.QUOTE_MINIMAL)
convert_to_writer.writerow(["Latitude", "Longitude", "Name", "Address", "City", "Postcode", "Network"])

with open(csv_list[int(file_to_convert)], mode="r") as convert_from:
    convert_from_reader = csv.reader(convert_from)

    for line in convert_from_reader:
        new_line = []
        new_line.append(line[0])
        new_line.append(line[1])
        new_line.append(line[2])
        line_anddress, line_city, line_post_code, line_network = line[2].split("; ")
        new_line = new_line + [line_anddress, line_city, line_post_code, line_network.strip("()")]
        convert_to_writer.writerow(new_line)


convert_to.close()
