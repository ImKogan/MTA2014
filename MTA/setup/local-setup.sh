#!/bin/bash

# linux-env setup
#sudo apt-get update
#sudo apt-get -y -q install \
#	binutils libproj-dev gdal-bin \
#	postgresql-client \
#	python3-pip
sudo apt-get -y -q install unzip protobuf-compiler

## setup python requirements
pip3 install -r ../requirements.txt
## get static data
bash get-static.sh
## make shapefiles from static data
bash make-shapefile.sh
## get mta realtime data
bash get-realtime.sh 100
#
## process realtime data into csv
python3 ../gtfs_to_csv_dir.py ../data/realtime
# make db migrations
bash migrate.sh
# load static data to db
bash load-static-db.sh
# load realtime data to db
python3 ../django_app/db_2014/trip_to_sql.py ../data
python3 ../django_app/db_2014/vehicle_to_sql.py ../data

# generate django secret key and update settings.ini
cd ../django_app/mta
python3 manage.py generate_secret_key --replace
sed -ir '/^SECRET_KEY/s/.*/SECRET_KEY: '"$(cat secretkey.txt)"'/' settings.ini
while [ $? -ne 0 ]; do
	python3 manage.py generate_secret_key --replace
	sed -ir '/^SECRET_KEY/s/.*/SECRET_KEY: '"$(cat secretkey.txt)"'/' settings.ini
done
rm -f secretkey.txt
rm -f settings.inir
echo secret key generated

