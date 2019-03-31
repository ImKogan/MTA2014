'''
load_shapes.py

upload shapes.shp (route locations) to db
'''

import os
import argparse
from django.contrib.gis.utils import LayerMapping
from .models import Shapes

shapes_mapping = {
    'shape_id': 'shape_id',
    'route_name': 'route_name',
    'geom': 'LINESTRING',
}

def run(args, verbose=True):
    '''function to run upload
    '''
    shapes_shp = args['path']
    lm = LayerMapping(Shapes, shapes_shp, shapes_mapping)

    lm.save(strict=True, verbose=verbose)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help="path to shapefile to insert into db")
    args = parser.parse_args()

    run(vars(args))

