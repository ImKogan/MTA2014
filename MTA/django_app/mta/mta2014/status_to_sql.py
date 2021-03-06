#!/usr/bin/python3
'''
status_to_sql.py

upload static routes csv to status table in db
'''

import os
import argparse
from configparser import RawConfigParser
import psycopg2

from . import db_conn

def run(args):
    '''run upload to db
    '''
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql = os.path.join(BASE, 'mta2014', 'sql', 'status.sql')
    with open(sql) as f:
        SQL = f.read()
    settings = os.path.join(BASE, args['settings'])
    DATABASE = db_conn.db_connection(settings)
    conn = psycopg2.connect(
        "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
    cur = conn.cursor()
    path = args['path']
    my_file = open(path)
    cur.copy_expert(
        sql=SQL.format('mta2014_status'),
        file=my_file)
    conn.commit()
    cur.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help="path to csv file to insert into db")
    parser.add_argument(
        '--settings', default='settings.ini', help="name of settings .ini file")
    args = parser.parse_args()
    
    run(vars(args))

