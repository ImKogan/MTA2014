'''
views.py

declare views
'''

from collections import defaultdict
from datetime import datetime, time, timedelta
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views import generic, View
from django.core.serializers import serialize
from django.db.models.functions import Lower, Substr
from django.db.models import F, Q, Max, Min
import pytz
from .models import NYCBoroughs, Stops, Shapes, Trip, RouteInfo, Date

class BorosListView(generic.ListView):
    '''Render page with NYC boro boundaries
    '''

    template_name = 'mta2014/nyb.html'
    #model = NYCBoroughs
    context_object_name = 'boros_list'

    def get_queryset(self):
        '''return json of queryset'''
        polygons = NYCBoroughs.objects.all()
        polygons_list = [poly.geom.geojson for poly in polygons]
        return polygons_list

class MapMTAView(View):
    '''Render initial page with NYC boros borders and subway lines and stops
    '''
    def __init__(self):
        self.template_name = 'mta2014/map_mta.html'

    def get(self, request):
        '''return json of queryset'''
        polygons = NYCBoroughs.objects.all()
        polygons_list = [poly.geom.geojson for poly in polygons]

        shapes = Shapes.objects.all()
        shapes_json = json.loads(serialize(
            'geojson', shapes, geometry_field='geom',
            fields=('shape_id', 'route_name')))

        routes = RouteInfo.objects.exclude(trip__isnull=True)
        route_names = [route['route_short_name'] for route in routes.values()]
        stops = Stops.objects.filter(location_type=1)
        stops_json = json.loads(serialize(
            'geojson', stops, geometry_field='geom',
            fields=('stop_id', 'stop_name', 'location_type', 'parent_station')))
        dates = Date.objects.aggregate(Min('date'), Max('date'))

        context = {'polygons_list': polygons_list,
                   'shapes_json': shapes_json,
                   'route_names': route_names,
                   'stops_json': stops_json,
                   'dates': dates,
                   'access_key': {'mapbox':settings.ACCESS_KEY}}
                   
        return render(request, self.template_name, context)

class RouteStopsView(View):
    '''Return json with arrival and departure times for selected route
    '''

    def get(self, request):
        route = request.GET['route']
        direction = request.GET['direction']
        date = request.GET['date']
        hour = request.GET['hour']
        print(route, direction, date, hour)

        start_stamp, end_stamp = date_to_stmps(date, hour)

        trips = Trip.objects.annotate(
            d=Lower(Substr('stop__stop_id', 4, 1)),
            r_route_id=F('route__route_id'),
            s_stop_id=F('stop__stop_id')).filter(
                (Q(arrival__lte=end_stamp) | Q(departure__lte=end_stamp)) &
                (Q(arrival__gte=start_stamp) | Q(departure__gte=start_stamp)),
                header_timestamp__timestamp__gte=start_stamp-300,
                header_timestamp__timestamp__lte=end_stamp+360,
                route__route_id=route,
                d=direction).order_by('stop__stop_id', 'arrival', 'departure')
        trips_values = trips.values(
            'stop_id', 'r_route_id', 's_stop_id', 'arrival', 'departure')
        print(len(trips_values))
        stop_ids = list(set([trip['stop_id'] for trip in trips_values]))
        stops = Stops.objects.filter(pk__in=stop_ids)
        stops_values = stops.values()
        print(len(stops))

        if len(trips.values()) == 0:
            message = "Your query returned 0 results"
            print(message)
            return JsonResponse({"message": message})
        trips_dict = defaultdict(list)
        for item in trips_values:
            trips_dict[item['s_stop_id']].append({
                'route_id': item['r_route_id'],
                'stop_id': item['s_stop_id'],
                'arrival': item['arrival'],
                'departure': item['departure']})

        stops_json = []
        for i in range(len(stops)):
            stops_json.append({
                "type": "Feature",
                "properties": {
                    "route_id": trips_dict[stops_values[i]['stop_id']][0]['route_id'],
                    "stop_id": stops_values[i]['stop_id'],
                    "name": stops_values[i]['stop_name'],
                    "date": date,
                    "stops_info": trips_dict[stops_values[i]['stop_id']]
                },
                "geometry": json.loads(stops[i].geom.geojson)
            })

        shapes = Shapes.objects.filter(route_name=route)
        print(len(shapes))
        shapes_json = json.loads(serialize(
            'geojson', shapes, geometry_field='geom',
            fields=('shape_id', 'route_name')))

        return JsonResponse({"stops_json": stops_json,
                             'shapes_json': shapes_json})

class StopTimesView(View):
    '''Return json with arrival and departure times for selected stop
    '''

    def get(self, request):
        stop = request.GET['stop']
        date = request.GET['date']
        hour = request.GET['hour']
        print(stop, date, hour)

        start_stamp, end_stamp = date_to_stmps(date, hour)
        stop_id = stop.split(":")[-1].strip()
        stop_id_n = stop_id+'N'
        stop_id_s = stop_id+'S'

        trips = Trip.objects.annotate(
            r_id=F('route__route_id'),
            s_id=F('stop__stop_id')).filter(
                Q(stop__stop_id=stop_id_n) | Q(stop__stop_id=stop_id_s),
                (Q(arrival__lte=end_stamp) | Q(departure__lte=end_stamp)) &
                (Q(arrival__gte=start_stamp) | Q(departure__gte=start_stamp)),
                header_timestamp__timestamp__gte=start_stamp-300,
                header_timestamp__timestamp__lte=end_stamp+360).order_by(
                    'arrival', 'departure')

        if len(trips.values()) == 0:
            message = "Your query returned 0 results"
            print(message)
            return JsonResponse({"message": message})

        stops = Stops.objects.filter(stop_id=stop_id)
        stops_json = json.loads(serialize(
            'geojson', stops, geometry_field='geom',
            fields=('stop_id', 'stop_name', 'location_type', 'parent_station')))
        trips_values = trips.values(
            'r_id', 's_id', 'arrival', 'departure')
        stops_json['features'][0]['properties']['date'] = date
        stops_json['features'][0]['properties']['trips'] =\
            [{'route_id':d['r_id'], 'stop_id':d['s_id'], 'arrival':d['arrival'],
              'departure':d['departure']} for d in list(trips_values)]
        return JsonResponse({"stops_json": stops_json})

def date_to_stmps(date, hour):
    '''return timestamp int for (date,hour)
    '''
    naive_date = datetime.strptime(date, '%Y-%m-%d')
    naive_datetime = datetime.combine(naive_date, time(int(hour)))
    eastern = pytz.timezone("US/Eastern")
    local_datetime = eastern.localize(naive_datetime)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    start_stamp = utc_datetime.timestamp()
    delta = timedelta(hours=1)
    end_utc_datetime = utc_datetime + delta
    end_stamp = end_utc_datetime.timestamp()

    return start_stamp, end_stamp

