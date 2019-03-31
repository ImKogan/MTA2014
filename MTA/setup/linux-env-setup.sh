#!/bin/bash
# setup.sh -- install linux requirements

apt-get -y -q update
apt-get -y -q install unzip protobuf-compiler postgresql postgresql-contrib \
	binutils libproj-dev gdal-bin postgresql-10-postgis-2.4 postgresql-10-postgis-scripts \
	python3-pip
