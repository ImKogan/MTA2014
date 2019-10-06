#!/usr/bin/python3

'''
gtfs_to_df.py

module to process gtfs-realtime files - ouputs pandas dataframes and saves to local directory
'''

import os
import json
from time import time
from collections import defaultdict
from glob import glob
import pandas as pd
from pprint import pprint
import proto.gtfs_realtime_pb2 as gtfs_rt
from google.protobuf.json_format import MessageToJson
from local_modules.mta_classes import TripUpdateUnpacked, Vehicle
from local_modules.functions import date_path_concat

def gtfs_to_df(gtfs_files, dataframes_dir, target_dir):
    '''call parse_update on each file in gtfs_files,
    save created df's in target_dir
    '''
    # master lists will contain data for the entire day
    master_trip_update_list = []
    # list pf 'vehicle' objects
    master_vehicle_list = []

    # loop over gtfs_files - convert to dict and append to appropriate list
    unparsable = 0
    for gtfs_file in gtfs_files:
        parse_update(gtfs_file, master_trip_update_list,
                     master_vehicle_list, unparsable)

    print('unparsable', unparsable)
    print('len(master_trip_update_list)', len(master_trip_update_list))
    print('len(master_vehicle_list)', len(master_vehicle_list))

    trip_update_df = pd.DataFrame(master_trip_update_list)
    vehicle_df = pd.DataFrame(master_vehicle_list)

    trip_col_mapping = {'header_timestamp':'header_timestamp',
                        'tripId':'trip_id',
                        'stopId':'stop_id',
                        'current_stop_id':'current_stop_id',
                        'routeId':'route_id',
                        'stop_number':'stop_number',
                        'startDate':'start_date',
                        'arrival':'arrival',
                        'departure':'departure',
                        'id':'update_id'}

    vehicle_col_mapping = {'header_timestamp': 'header_timestamp',
                           'tripId':'trip_id',
                           'stopId':'stop_id',
                           'timestamp':'timestamp',
                           'currentStatus':'current_status',
                           'currentStopSequence':'current_stop_sequence',
                           'routeId':'route_id',
                           'startDate':'start_date',
                           'id':'updateid'}

    trip_update_df.rename(columns=trip_col_mapping, inplace=True)
    vehicle_df.rename(columns=vehicle_col_mapping, inplace=True)

    trip_update_cols = [
        'header_timestamp', 'update_id', 'trip_id',
        'route_id', 'stop_id', 'current_stop_id', 'stop_number',
        'start_date', 'arrival', 'departure']
    trip_update_df = trip_update_df[trip_update_cols]

    if not os.path.exists(dataframes_dir):
        os.mkdir(dataframes_dir)
    if not os.path.exists(os.path.join(dataframes_dir, target_dir)):
        os.mkdir(os.path.join(dataframes_dir, target_dir))
    file_dir = dataframes_dir + '/' + target_dir

    vehicle_df.drop(vehicle_df[vehicle_df['timestamp'].isna()].index, inplace=True)
    trip_update_df.to_csv(os.path.join(file_dir, 'trip_update.csv'), index=False)
    vehicle_df.to_csv(os.path.join(file_dir, 'vehicle.csv'), index=False)

def get_gtfs_files(unzip_dir, gtfs_dir):
    '''build gtfs_files list for gtfs_dir
    '''
    gtfs_dir_path = unzip_dir+'/'+gtfs_dir
    gtfs_files1 = glob(os.path.join(gtfs_dir_path, 'gtfs-2*'))
    gtfs_files2 = glob(os.path.join(gtfs_dir_path, 'gtfs-l*'))
    # gtfs_files is glob list of file paths that we want to analyze
    gtfs_files = gtfs_files1 + gtfs_files2
    gtfs_files.sort()
    print(len(gtfs_files))

    return gtfs_files
    
def get_gtfs_dir(realtime_date):
    '''build list of gtfs file paths for given date
    '''
    # local directory stroing gtfs-realtime files for a given date
    unzip_dir = 'gtfs_rt_'+str(realtime_date[0])+'_unzipped'
    gtfs_dir = unzip_dir+'/'+'gtfs_rt_'+date_path_concat(*realtime_date)
    gtfs_files1 = glob(os.path.join(gtfs_dir, 'gtfs-2*'))
    gtfs_files2 = glob(os.path.join(gtfs_dir, 'gtfs-l*'))
    # gtfs_files is glob list of file paths that we want to analyze
    gtfs_files = gtfs_files1 + gtfs_files2
    gtfs_files.sort()
    print(len(gtfs_files))

    return gtfs_files

def parse_update(gtfs_file, master_trip_update_list,
                 master_vehicle_list, unparsable):
    '''parse gtfs_file into a dictionary, call unpack_update,
    update master list, or increment unparsable
    '''
    print(gtfs_file)
    t1 = time()
    f = open(gtfs_file, 'rb')
    raw_str = f.read()
    msg = gtfs_rt.FeedMessage()
    try:
        msg.ParseFromString(raw_str)
        json_obj = MessageToJson(msg)
        data_dict = json.loads(json_obj)
    except:
        unparsable += 1
        return

    if not data_dict:
        return

    trip_update_list, vehicle_list = unpack_update(data_dict)

    master_trip_update_list.extend(trip_update_list)
    master_vehicle_list.extend(vehicle_list)
    t2 = time()
    print(t2 -t1)

def unpack_update(data_dict):
    '''unpack data_dict into structured format of list of dicts
    '''
    # list of 'tripUpdate' objects
    trip_update_list = []
    # list of 'vehicle' objects
    vehicle_list = []
    for i in range(len(data_dict['entity'])):
        # if data_dict['entity'] is a 'tripUpdate' object
        if data_dict['entity'][i].get('tripUpdate'):
            trip = data_dict['entity'][i]
            if trip['tripUpdate'].get('stopTimeUpdate'):
                stops = len(trip['tripUpdate']['stopTimeUpdate'])
                for i in range(stops):
                    trip_update_list.append(
                        TripUpdateUnpacked(
                            data_dict['header'],
                            trip,
                            i).dict_row()
                        )

        # if data_dict['entity'] is a 'vehicle' object
        elif data_dict['entity'][i].get('vehicle'):
            vehicle = data_dict['entity'][i]
            vehicle_list.append(
                Vehicle(data_dict['header'], vehicle).dict_row())

    return trip_update_list, vehicle_list

if __name__ == '__main__':
    realtime_date = (2014, 9, 30)
    dataframes_dir = 'raw_frames'
    target_dir = date_path_concat(*realtime_date)
    t = time()
    gtfs_files = get_gtfs_dir(realtime_date)
    gtfs_to_df(gtfs_files, dataframes_dir, target_dir)
    print(time() - t)

