#! /usr/bin/python3
## Short script to convert ASCII.csv to ASCII_Translator.py that contains ascii_dict with all values.
## It is used in shell_coordinates_extractor

import csv
import pprint as pp

ascii_dict = dict()

with open("ASCII.csv", mode="r") as ascii_csv_file:
# Opens csv file
    ascii_csv_file_reader = csv.reader(ascii_csv_file)
    for line in ascii_csv_file_reader:
        ascii_dict[int(line[0])] = int(line[1])

ASCII_Translator = open("ASCII_Translator.py", mode="w")

ASCII_Translator.write("ascii_dict = " + pp.pformat(ascii_dict) + "\n")

ASCII_Translator.close()