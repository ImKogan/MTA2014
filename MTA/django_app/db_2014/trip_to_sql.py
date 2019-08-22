#!/usr/bin/python3

'''
trip_to_sql.py

module to load gtfs-realtime tabular data to db
'''

import os
from collections import OrderedDict
from glob import glob
import argparse
from configparser import RawConfigParser
import psycopg2
import pandas as pd
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('dir', help="directory to reatime csv's")
args = parser.parse_args()
DIR = args.dir

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = RawConfigParser()
config.read(os.path.join(BASE, 'mta', 'db-settings.ini'))
DATABASE = {'HOST': config.get('database', 'DATABASE_HOST'),
            'PORT': config.get('database', 'DATABASE_PORT'),
            'NAME': config.get('database', 'DATABASE_NAME'),
            'USER': config.get('database', 'DATABASE_USER'),
            'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
           }

g = glob(os.path.join(DIR, 'raw_frames', '*'))
g.sort()
print(g)

CREATE_STATEMENT = '''
        CREATE TEMPORARY TABLE temp (
                header_timestamp INTEGER,
                updateid INTEGER,
                trip TEXT,
                route TEXT,
                stop TEXT,
                current_stop TEXT,
                stop_number INTEGER,
                start_date INTEGER,
                arrival FLOAT,
                departure FLOAT)
'''

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
with open(os.path.join(dname, 'trip.sql')) as f:
    SQL_STATEMENT = f.read()

cols = ['header_timestamp_id', 'updateid', 'trip_id', 'route_id',
        'stop_id', 'current_stop_id', 'stop_number', 'start_date_id',
        'arrival', 'departure']

cols_dict = OrderedDict()
for item in cols:
    if item[-3:] == '_id':
        cols_dict[item] = item[:-3]
    else:
        cols_dict[item] = item

temp_cols = [cols_dict[k] for k in cols_dict]

def process_file(conn, CREATE_STATEMENT, SQL_STATEMENT, table_name,
                 cols, temp_cols, cols_dict, file_object):
    '''upload csv file to staging table and normalize to query tables
    '''
    cur = conn.cursor()
    cur.execute(CREATE_STATEMENT)
    cur.copy_expert(
        sql=SQL_STATEMENT.format(
            ', '.join(temp_cols),
            table_name,
            ', '.join(cols),
            **cols_dict),
        file=file_object)
    cur.execute('DROP TABLE temp;')
    conn.commit()
    cur.close()

t = time()
conn = psycopg2.connect(
    "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
try:
    for path in g:
        csv_path = os.path.join(path, 'trip_update.csv')
        table = 'mta2014_trip'
        print(CREATE_STATEMENT)
        print(SQL_STATEMENT.format(', '.join(temp_cols),
            table, ', '.join(cols), **cols_dict))
        my_file = open(csv_path)
        t1 = time()
        try:
            process_file(conn, CREATE_STATEMENT, SQL_STATEMENT,
                table, cols, temp_cols, cols_dict, my_file)
            print(time() - t1)
            print(path)
        finally:
            my_file.close()
finally: 
    conn.close()
print(time() - t)

