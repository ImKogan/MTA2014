#!/usr/bin/python3
'''
create_index.py

create unique index in mta2014_trip table on (start_date, trip_id, stop_id)
'''

import os
from configparser import RawConfigParser
import psycopg2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = RawConfigParser()
config.read(os.path.join(BASE, 'settings.ini'))
DATABASE = {'HOST': config.get('database', 'DATABASE_HOST'),
            'PORT': config.get('database', 'DATABASE_PORT'),
            'NAME': config.get('database', 'DATABASE_NAME'),
            'USER': config.get('database', 'DATABASE_USER'),
            'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
           }

sql = os.path.join(BASE, 'mta2014', 'sql', 'create_index.sql')
with open(sql) as f:
    SQL = f.read()

conn = psycopg2.connect(
    "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
cur = conn.cursor()
cur.execute(SQL)
conn.commit()
cur.close()
