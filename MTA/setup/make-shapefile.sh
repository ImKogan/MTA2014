#!/bin/bash
# make-shapefile.sh -- process some of the static data into shapefiles
# vim: ts=2 sw=2 sws=2 expandtab

set -uxe

DATA_DIR="data"
STATIC="static"
SHAPEFILES="shapefiles"

cd "$(dirname "$0")"
pushd ..

# create dirs if they dne
mkdir -p "$DATA_DIR/$STATIC/$SHAPEFILES"

python3 shapes_csv_to_shp.py $DATA_DIR/$STATIC/gtfs_static/shapes.txt
python3 stops_csv_to_shp.py $DATA_DIR/$STATIC/gtfs_static/stops.txt

popd
