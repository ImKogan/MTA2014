#!/bin/bash
# load-static-db.sh -- load static data to db

cd "$(dirname "$0")"
pushd ../django_app/mta
pwd

./manage.py populate_db ../../data/static/gtfs_static/status.txt status_to_sql
./manage.py populate_db ../../data/static/gtfs_static/routes.txt routes_to_sql
./manage.py populate_db ../../data/static/nybb_19a/nybb.shp load_boros
./manage.py populate_db ../../data/shapefiles/stops.shp load_stops
./manage.py populate_db ../../data/shapefiles/shapes.shp load_shapes
