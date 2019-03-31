'''
load_stops.py

upload stops.shp (stop locations) to db
'''

import os
import argparse
from django.contrib.gis.utils import LayerMapping
from .models import Stops

stops_mapping = {
    'stop_id': 'stop_id',
    'stop_code': 'stop_code',
    'stop_name': 'stop_name',
    'stop_desc': 'stop_desc',
    'zone_id': 'zone_id',
    'stop_url': 'stop_url',
    'location_type': 'location_ty',
    'parent_station': 'parent_stat',
    'geom': 'POINT',
}

def run(args, verbose=True):
    '''function to run upload
    '''
    stops_shp = args['path']
    lm = LayerMapping(Stops, stops_shp, stops_mapping)

    lm.save(strict=True, verbose=verbose)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help="path to shapefile to insert into db")
    args = parser.parse_args()

    run(vars(args))

