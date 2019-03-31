'''
mta_classes.py

module defines 2 classses that convert gtfs objects to python dict
'''

class TripUpdateUnpacked:
    ''' arguments: header, tripupdate, i
    converts tripUpdate object to Class with the necessary data fields
    as attributes.
    '''
    def __init__(self, header, tripupdate, i):
        self.header_timestamp = header['timestamp']
        self.id = tripupdate['id']
        self.stop_number = i
        self.current_stop_id = tripupdate['tripUpdate']['stopTimeUpdate'][0].\
            get('stopId')
        self.arrival = tripupdate['tripUpdate']['stopTimeUpdate'][i].get(
            'arrival', {}).get('time')
        self.departure = tripupdate['tripUpdate']['stopTimeUpdate'][i].get(
            'departure', {}).get('time')
        self.stopId = tripupdate['tripUpdate']['stopTimeUpdate'][i].get('stopId')
        self.routeId = tripupdate['tripUpdate']['trip']['routeId']
        self.startDate = tripupdate['tripUpdate']['trip']['startDate']
        self.tripId = tripupdate['tripUpdate']['trip']['tripId']

    def dict_row(self):
        '''returns dict with class atributes as keys and corresponding values
        '''
        dict_row = {}
        for var in vars(self):
            if var != 'dict_row':
                dict_row[var] = getattr(self, var)
        return dict_row

class TripUpdate:
    ''' arguments: header, tripupdate
    converts tripUpdate object to Class with the necessary data fields
    as attributes.
    '''
    def __init__(self, header, tripupdate):
        self.header_timestamp = header['timestamp']
        self.id = tripupdate['id']
        self.stopTimeUpdate = tripupdate['tripUpdate']['stopTimeUpdate']
        self.stopId = tripupdate['tripUpdate']['stopTimeUpdate'][0].get('stopId')
        self.routeId = tripupdate['tripUpdate']['trip']['routeId']
        self.startDate = tripupdate['tripUpdate']['trip']['startDate']
        self.tripId = tripupdate['tripUpdate']['trip']['tripId']

    def dict_row(self):
        '''returns dict with class atributes as keys and corresponding values
        '''
        dict_row = {}
        for var in vars(self):
            if var != 'dict_row':
                dict_row[var] = getattr(self, var)
        return dict_row

class Vehicle:
    ''' arguments: header, vehicle
    converts Vehicle object to Class with the necessary data fields
    as attributes.
    '''
    def __init__(self, header, vehicle):
        self.header_timestamp = header['timestamp']
        self.id = vehicle['id']
        self.currentStatus = vehicle['vehicle'].get('currentStatus')
        self.currentStopSequence = vehicle['vehicle'].get('currentStopSequence')
        self.stopId = vehicle['vehicle'].get('stopId')
        self.timestamp = vehicle['vehicle'].get('timestamp')
        self.routeId = vehicle['vehicle']['trip']['routeId']
        self.startDate = vehicle['vehicle']['trip']['startDate']
        self.tripId = vehicle['vehicle']['trip']['tripId']

    def dict_row(self):
        '''returns dict with class atributes as keys and corresponding values
        '''
        dict_row = {}
        for var in vars(self):
            if var != 'dict_row':
                dict_row[var] = getattr(self, var)
        return dict_row
