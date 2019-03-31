#!/bin/bash
# migrate.sh make -- initiate django db migrations and create index

cd "$(dirname "$0")"
pushd ../django_app/mta/
./manage.py migrate
./manage.py makemigrations
./manage.py migrate
./mta2014/create_index.py
