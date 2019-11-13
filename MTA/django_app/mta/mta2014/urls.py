from django.urls import path

from . import views

app_name = 'mta2014'
urlpatterns = [
    path('nyb', views.BorosListView.as_view(), name='nyb'),
    path('map_mta', views.MapMTAView.as_view(), name='map_mta'),
    path('route_stops', views.RouteStopsView.as_view(), name='route_stops'),
    path('stop_times', views.StopTimesView.as_view(), name='stop_times'),
    path('query_mta', views.Query.as_view(), name='query_mta'),
    path('query_trips', views.QueryTrips.as_view(), name='query_trips'),
]
