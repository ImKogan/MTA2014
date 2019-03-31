#!/usr/bin/python3
'''
stops_csv_to_shp.py

convert stops.csv to shapefile format
'''


# import libraries
import os
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
output_shp = shapefile.Writer(shapefile.POINT)
# for every record there must be a corresponding geometry.
output_shp.autoBalance = 1
# create the field names and data type for each.
# you can insert or omit lat-long here
output_shp.field('stop_id', 'C')
output_shp.field('stop_code', 'C')
output_shp.field('stop_name', 'C')
output_shp.field('stop_desc', 'C')
output_shp.field('zone_id', 'C')
output_shp.field('stop_url', 'C')
output_shp.field('location_type', 'C')
output_shp.field('parent_station', 'C')
# count the features
counter = 1
# access the CSV file
with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # skip the header
    next(reader, None)
    #loop through each of the rows and assign the attributes to variables
    for row in reader:
        stop_id = row[0]
        stop_code = row[1]
        stop_name = row[2]
        stop_desc = row[3]
        zone_id = row[6]
        stop_url = row[7]
        location_type = row[8]
        parent_station = row[9]
        stop_lat = row[4]
        stop_lon = row[5]

        # create the point geometry
        output_shp.point(float(stop_lon), float(stop_lat))
        # add attribute data
        output_shp.record(
            stop_id, stop_code, stop_name, stop_desc,
            zone_id, stop_url, location_type, parent_station)
        print("Feature " + str(counter) + " added to Shapefile.")
        counter = counter + 1
# save the Shapefile
SHAPEFILE_DIR = 'shapefiles'
if not os.path.exists(os.path.join('data', SHAPEFILE_DIR)):
    os.mkdir(os.path.join('data', SHAPEFILE_DIR))
output_shp.save(os.path.join('data', SHAPEFILE_DIR, 'stops.shp'))

PRJ = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
with open(os.path.join('data', SHAPEFILE_DIR, 'stops.prj'), 'w') as prj:
    prj.write(PRJ)
