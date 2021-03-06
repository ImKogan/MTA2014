# MTA2014


MTA2014 is a django app which provides a web interface for looking up
historical MTA Subway train data.

## Try it!

MTA2014 uses Mapbox to provide the map which serves as the backdrop for the
map of the subway. Installing MTA2014 is simple but requires first signing
up for Mapbox, and getting an API key.

* [Mapbox](https://mapbox.com)
* [Create](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#creating-and-managing-access-tokens) a Mapbox API key.
* After cloning the repo, cd into  
`MTA2014/MTA/django_app/mta`  
and copy `temp_setting.ini` to `settings.ini`  
`cp temp_setting.ini settings.ini`  
edit the new `settings.ini` file by updating the ACCESS_KEY value.
```
[database]
..........
..........
[secrets]
SECRET_KEY: <Django SECRET KEY>
ACCESS_KEY: <MAPBOX API KEY>
```
and update you local database credentials from defaults if desired.

At this point there are two ways to configure the app:
##### Directly on your machine:
* cd into setup directory
`MTA2014/MTA/setup`  
open `local-setup.sh` \
Lines 4-9 install postgresql-client and a few other dependencies needed to use postgis. \
If you already have these libraries, do not uncomment the lines. \
While these packages are those installed on my machine (Ubuntu 18.04) I haven't tested this in general.
* Having either uncommented (to install upon running now, or relying on preinstalled packages), check line 19 in this file. If running a demo, it is advised to change the 100 to a smaller number (such as 5). This argument is the number of days of data to be downloaded. If left at a 100 - the complete process will take at least a half hour (on any reasonable personal machine).
* Configure your postgres DATABASE. MAKE SURE THE REDENTIALS MATCH THE settings.ini FILE ABOVE.
* Don't forget to create a postgis extension
`CREATE EXTENSION postgis;`
(Unless you have created a superuser for this db - you will need to access the db as a superuser to create an extension)
* Finally, run
`. local-setup.sh`
* in `MTA2014/MTA/django_app/mta` run:
` ./manage.py runserver`
* In the browser: `http://127.0.0.1:8000/mta2014/map_mta` \
Remember to use chrome! Currently the 'Map' and 'Query' tabs are confifured.

##### On a VirtualBox using Vagrant:
* Install [Vagrant and Virtualbox](https://www.vagrantup.com/intro/getting-started/) (`sudo apt-get install virtualbox` `sudo apt-get install vagrant`)
* cd into the repo root folder MTA2014/ and run `vagrant up`.
* This will create a new virtualbox and install all the necessary dependencies
on it. The project's data will be downloaded and the database configured.
* Note: In the previous step - the default is to download only 2 days worth of data in order to expedite configuration time. To change the default and to download all available (historical mta 2014 data), BEFORE running the `vagrant up` command, edit the Vagrantfile in line 5 by changing the `data_size` variable from "short" to "full".
* ssh into the vm by running `vagrant ssh`
* In the vm, run `cd /vagrant/MTA/django_app/mta`
* Then launch the django server by running `python3 manage.py runserver 0.0.0.0:8000`
* Finally, in the host machine, type `http://localhost:8001/mta2014/map_mta` in your browser.

## Data Source

The [MTA Real-Time Data Feeds](http://datamine.mta.info/) provides
GTFS structured data of live train traffic. This data feed is used universally:
on the MTA website, station platforms, and is ingested by Google Maps. In this
initial version of the application, we use historical data from 2014 stored in
an AWS-S3 bucket instead of recent data. [MTA Historical GTFS-realtime data](http://web.mta.info/developers/MTA-Subway-Time-historical-data.html).
This data runs from September-December 2014 for the subway lines 1,2,3,4,5,6,S,L, and is the data used for the current stage of this project.

GTFS (General Transit Feed Specification) is an open data format for public transportation. 
More information can be found here:

* [GTFS Realtime protobufs](https://developers.google.com/transit/gtfs-realtime/).
* [MTA's specs](http://datamine.mta.info/sites/all/files/pdfs/GTFS-Realtime-NYC-Subway%20version%201%20dated%207%20Sep.pdf).

## Technology used

The app is written in Python using
Django/[Geodjango](https://docs.djangoproject.com/en/2.1/ref/contrib/gis/).

The database uses [PostGIS](https://postgis.net/), a spatial database extension for PostgreSQL.

The Django app depends on the train information to be stored in the database.
The ingestion of the GTFS data is done by our python script `gtfs_to_csv.py`
using standard protobuf libraries and Pandas.

The front-end depends on the popular location platform provided by [Mapbox](https://mapbox.com).
The app's features on the map are rendered by [LeafletJS](https://leafletjs.com/), a mature library based on D3.js.

The front-end framework is [Materialize](https://materializecss.com/).

## Current state and further development
* Currently, the application is static, as it ingests the MTA's historical data. The goal is to use this stage of the project as a testing environment for processing and serving the MTA's current subway data.
* While the historical data is available only for some lines, the current data is system-wide.
* Currently, the application is a reporting visualization tool. A user can visualize, on a map, the departure and arrival times for a given line (during a specified time interval) or a given station. 
* The next phase will see the database exposed for querying. This will allow for users to explore the data on their own. Concurrently, we plan to offer some of our own analysis of the data. More details will follow as the project progresses.
* The application will eventually serve 3 functions:
  * Users will be able to visualize past arrival and departure times for the entire subway system.
  * For researchers, our database will provide tabular data produced by the ETL process we implement.
  * We will offer results of our own data exploration analysis and visualization. This is the most interesting and exciting aspect of this application. 
