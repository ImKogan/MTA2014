'''
models.py

declare db models
'''

#from django.db import models
from django.contrib.gis.db import models
#from datetime import datetime
from django.utils import timezone
#from django.db.models.functions import Now

class Trip(models.Model):
    '''main table for trip updates
    '''
    header_timestamp = models.ForeignKey('Timestamp', on_delete=models.CASCADE)
    updateid = models.IntegerField()
    trip = models.ForeignKey('TripName', on_delete=models.CASCADE)
    route = models.ForeignKey('RouteInfo', on_delete=models.CASCADE, null=True)
    stop = models.ForeignKey(
        'Stops',
        on_delete=models.CASCADE,
        related_name='stop_trips', null=True)
    current_stop = models.ForeignKey(
        'Stops',
        on_delete=models.CASCADE,
        related_name='current_stop_trips', null=True)
    stop_number = models.IntegerField()
    start_date = models.ForeignKey('Date', on_delete=models.CASCADE)
    arrival = models.FloatField(null=True)
    departure = models.FloatField(null=True)
    created = models.DateTimeField(default=timezone.now)

class Timestamp(models.Model):
    '''parent table for trip storing timestamps (of trip updates)
    '''
    timestamp = models.IntegerField()

class Date(models.Model):
    '''parent table for trip storing date column
    '''
    date = models.IntegerField()

class TripName(models.Model):
    '''parent table for trip storing trip column (trip_id)
    '''
    trip_name = models.CharField(max_length=32)

class RouteInfo(models.Model):
    '''stores routeinfo from static-gtfs routes file
    '''
    route_id = models.CharField(max_length=4)
    agency_id = models.CharField(max_length=32)
    route_short_name = models.CharField(max_length=4)
    route_long_name = models.CharField(max_length=64)
    route_desc = models.CharField(max_length=4096)
    route_type = models.IntegerField()
    route_url = models.CharField(max_length=128)
    route_color = models.CharField(max_length=16, null=True)
    route_text_color = models.CharField(max_length=16, null=True)

# This is an auto-generated Django model module created by ogrinspect.

class NYCBoroughs(models.Model):
    '''NYC boros boundaries
    '''
    borocode = models.IntegerField()
    boroname = models.CharField(max_length=32)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for nybb model
nycboroughs_mapping = {
    'borocode': 'BoroCode',
    'boroname': 'BoroName',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}

# This is an auto-generated Django model module created by ogrinspect.

class Stops(models.Model):
    '''stop locations from static-gtfs stops file
    '''
    stop_id = models.CharField(max_length=50)
    stop_code = models.CharField(max_length=50)
    stop_name = models.CharField(max_length=50)
    stop_desc = models.CharField(max_length=50)
    zone_id = models.CharField(max_length=50)
    stop_url = models.CharField(max_length=50)
    location_type = models.IntegerField()
    parent_station = models.CharField(max_length=50)
    geom = models.PointField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Stops model
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

# This is an auto-generated Django model module created by ogrinspect.

class Shapes(models.Model):
    '''route locations from static-gtfs shapes file
    '''
    shape_id = models.CharField(max_length=50)
    route_name = models.CharField(max_length=4)
    geom = models.LineStringField(srid=4326)
    routeinfo = models.ForeignKey('RouteInfo', null=True, on_delete=models.CASCADE)

# Auto-generated `LayerMapping` dictionary for Shapes model
shapes_mapping = {
    'shape_id': 'shape_id',
    'route_name': 'route_name',
    'geom': 'LINESTRING',
}
