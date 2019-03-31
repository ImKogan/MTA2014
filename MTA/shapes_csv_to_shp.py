#!/usr/bin/python3
'''
shapes_csv_to_shp.py

convert shapes.csv to shapefile format
'''

# import libraries
import os
from collections import defaultdict
import csv
import argparse
import shapefile

# get the path for the input_file (csv)
parser = argparse.ArgumentParser()
parser.add_argument(
    'input', help="path to input file to convert to shapefile")
args = parser.parse_args()
input_file = args.input

# create a point shapefile
output_shp = shapefile.Writer(shapefile.POLYLINE)
# for every record there must be a corresponding geometry.
output_shp.autoBalance = 1
# create the field names and data type for each.
# you can insert or omit lat-long here
output_shp.field('shape_id', 'C')
output_shp.field('route_name', 'C')
# count the features
counter = 1
# access the CSV file
d = defaultdict(list)
with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # skip the header
    next(reader, None)
    #loop through each of the rows and assign the attributes to variables
    for row in reader:
        d[row[0]].append([float(row[2]), float(row[1])])

    for k in d:
        shape_id = k
        route_name = k.split('.')[0]

        # create the line geometry
        output_shp.line(parts=[d[k]])
        # add attribute data
        output_shp.record(shape_id, route_name)
        print("Feature " + str(counter) + " added to Shapefile.")
        counter = counter + 1
# save the Shapefile
SHAPEFILE_DIR = 'shapefiles'
if not os.path.exists(os.path.join('data', SHAPEFILE_DIR)):
    os.mkdir(os.path.join('data', SHAPEFILE_DIR))
output_shp.save(os.path.join('data', SHAPEFILE_DIR, 'shapes.shp'))

PRJ = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
with open(os.path.join('data', SHAPEFILE_DIR, 'shapes.prj'), 'w') as prj:
    prj.write(PRJ)
