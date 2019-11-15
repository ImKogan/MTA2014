'''
populate_db.py

populate db with static data (nyc_boros, routes, stops, shapes)
'''

import argparse
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'command for initial db population'

    def add_arguments(self, parser):
        parser.add_argument('path', help = "path to file passed int load module")
        parser.add_argument('module', help="module to run")
        parser.add_argument('-s', default='settings.ini', help="name of settings .ini file")

    def handle(self, *args, **kwargs):
        print(args)
        print(kwargs)
        module = kwargs['module']
        if module == 'routes_to_sql':
            from ... import routes_to_sql
            kwargs['settings'] = kwargs['s']
            routes_to_sql.run(kwargs)
        if module == 'load_boros':
            from ... import load_boros
            load_boros.run(kwargs)
        if module == 'load_stops':
            from ... import load_stops
            load_stops.run(kwargs)
        if module == 'load_shapes':
            from ... import load_shapes
            load_shapes.run(kwargs)
        if module == 'status_to_sql':
            from ... import status_to_sql
            kwargs['settings'] = kwargs['s']
            status_to_sql.run(kwargs)
        print('Database updated succesfully'.center(50, '-'))

