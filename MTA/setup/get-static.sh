#!/bin/bash
# get-static.sh -- get static data from internet
# vim: ts=2 sw=2 sws=2 expandtab

set -uxe

DATA_DIR="data"
GET_STATIC=true
WGET="wget --quiet --no-clobber"

cd "$(dirname "$0")"
pushd ..

# create dirs if they dne
mkdir -p "proto" "$DATA_DIR/static"

# get gtfs protobuf definition 
pushd "proto"
$WGET -O "gtfs-realtime.proto" 'https://developers.google.com/transit/gtfs-realtime/gtfs-realtime.proto' || true
protoc -I=. --python_out=. gtfs-realtime.proto
popd

pushd "$DATA_DIR"
pwd

# get static data:
if $GET_STATIC; then
  pushd "static"
  # stop location, route location, etc.
  $WGET -O "gtfs_static.zip" 'http://transitfeeds.com/p/mta/79/1417752606/download' || true
  unzip -o "gtfs_static.zip" -d "gtfs_static"

  # nyc geographic boundaries
  $WGET -O "nybb_19a.zip"  'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nybb_19a.zip' || true
  unzip -o "nybb_19a.zip"
fi
popd
