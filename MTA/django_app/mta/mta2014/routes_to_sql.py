#!/usr/bin/python3
'''
routes_to_sql.py

upload static routes csv to routeinfo table in db
'''

import os
import argparse
from configparser import RawConfigParser
import psycopg2

def run(args):
    '''run upload to db
    '''
    path = args['path']
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = RawConfigParser()
    config.read(os.path.join(BASE, 'db-settings.ini'))
    DATABASE = {'HOST': config.get('database', 'DATABASE_HOST'),
                'PORT': config.get('database', 'DATABASE_PORT'),
                'NAME': config.get('database', 'DATABASE_NAME'),
                'USER': config.get('database', 'DATABASE_USER'),
                'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
               }

    sql = os.path.join(BASE, 'mta2014', 'sql', 'route_info.sql')
    with open(sql) as f:
        SQL = f.read()
    
    conn = psycopg2.connect(
        "host={HOST} port={PORT} dbname={NAME} user={USER} password={PASSWORD}".format(**DATABASE))
    cur = conn.cursor()
    my_file = open(path)
    cur.copy_expert(
        sql=SQL.format('mta2014_routeinfo'),
        file=my_file)
    conn.commit()
    cur.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help="path to csv file to insert into db")
    args = parser.parse_args()
    
    run(vars(args))

