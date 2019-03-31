'''
load_boros.py

upload nybb.shp to db (NYC boundaries)
'''

import os
import argparse
from django.contrib.gis.utils import LayerMapping
from .models import NYCBoroughs

nycboroughs_mapping = {
    'borocode': 'BoroCode',
    'boroname': 'BoroName',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}


def run(args, verbose=True):
    '''function to run upload
    '''
    nyb_shp = args['path']
    lm = LayerMapping(NYCBoroughs, nyb_shp, nycboroughs_mapping)

    lm.save(strict=True, verbose=verbose)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help="path to shapefile to insert into db")
    args = parser.parse_args()

    run(vars(args))

