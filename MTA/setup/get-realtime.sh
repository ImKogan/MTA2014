#!/bin/bash
# get-realtime.sh -- get project data from internet
# vim: ts=2 sw=2 sws=2 expandtab

set -uxe

DATA_DIR="data"
DAY_COUNT="$1"
START_DATE="2014-10-01"
WGET="wget --quiet --no-clobber"
REALTIME="realtime"
REALTIME_ZIP="realtime_zip"

if [[ $DAY_COUNT == "" ]]; then
  echo "Get MTA's gtfs realtime data"
  echo "usage: bash setup-mta.sh [number of days]"
fi

cd "$(dirname "$0")"
pushd ..
# create dirs if they dne
mkdir -p "$DATA_DIR/$REALTIME" "$DATA_DIR/$REALTIME_ZIP"
pushd "$DATA_DIR"
pwd

# get realtime data
pushd "$REALTIME_ZIP"
for i in $(seq $DAY_COUNT); do
  d=$(date -d "$START_DATE + $i days" -I)
  zipfile="gtfs_rt$d.zip"
  if test -f $zipfile; then
    continue;
  fi
  dirname="gtfs_rt_$d"
  url="https://datamine-$d.s3.amazonaws.com/gtfs.tgz"
  $WGET -O "$zipfile" "$url" || echo "failed to get day $d"
  if test -s $zipfile; then
    mkdir -p "$dirname"
    tar -xzf "$zipfile" -C "$dirname"
    mv "$dirname" "../$REALTIME/$dirname"
  elif test -e $zipfile; then
    rm $zipfile
  fi
done
popd

