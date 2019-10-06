#!/usr/bin/python3
'''
create_index.py

create unique index in mta2014_trip table on (start_date, trip_id, stop_id)
'''

import os
import argparse
from configparser import RawConfigParser
import psycopg2

from db_conn import db_connection

parser = argparse.ArgumentParser()
parser.add_argument(
    '--settings', default='settings.ini', help="name of settings .ini file")
args = parser.parse_args()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sql = os.path.join(BASE, 'mta2014', 'sql', 'create_index.sql')
with open(sql) as f:
    SQL = f.read()

settings = path['settings']
DATABASE = db_connection(settings)
conn = psycopg2.connect(
    "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
cur = conn.cursor()
cur.execute(SQL)
conn.commit()
cur.close()
