#!/usr/bin/python3
'''
create_index.py

create unique index in mta2014_trip table on (start_date, trip_id, stop_id)
'''

import os
from configparser import RawConfigParser
import psycopg2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection
    db_config = RawConfigParser()
    db_config.read(os.path.join(BASE, 'db-settings.ini.app'))

    DATABASE = {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': db_config.get('database', 'DATABASE_HOST'),
            'NAME': db_config.get('database', 'DATABASE_NAME'),
            'USER': db_config.get('database', 'DATABASE_USER'),
            'PASSWORD': db_config.get('database', 'DATABASE_PASSWORD'),
    }
else:
    # Running locally so connect to either a local Postgres instance or connect
    # to Cloud SQL via the proxy.  To start the proxy via command line:
    # $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    db_config = RawConfigParser()
    db_config.read(os.path.join(BASE, 'db-settings.ini'))

    DATABASE = {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': db_config.get('database', 'DATABASE_HOST'),
            'PORT': db_config.get('database', 'DATABASE_PORT'),
            'NAME': db_config.get('database', 'DATABASE_NAME'),
            'USER': db_config.get('database', 'DATABASE_USER'),
            'PASSWORD': db_config.get('database', 'DATABASE_PASSWORD'),
    }
# [END db_setup]

#config = RawConfigParser()
#config.read(os.path.join(BASE, 'settings.ini'))
#DATABASE = {'HOST': config.get('database', 'DATABASE_HOST'),
#            'PORT': config.get('database', 'DATABASE_PORT'),
#            'NAME': config.get('database', 'DATABASE_NAME'),
#            'USER': config.get('database', 'DATABASE_USER'),
#            'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
#           }

sql = os.path.join(BASE, 'mta2014', 'sql', 'create_index.sql')
with open(sql) as f:
    SQL = f.read()

conn = psycopg2.connect(
    "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
cur = conn.cursor()
cur.execute(SQL)
conn.commit()
cur.close()
