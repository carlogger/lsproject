#!/usr/bin/python

import csv
import sys

filename = sys.argv[1]
newcsv = []


with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        newcsv.append(row)
        newcsv[-1][0] = len(newcsv)-1

with open(filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',')
    csvwriter.writerows(newcsv)
