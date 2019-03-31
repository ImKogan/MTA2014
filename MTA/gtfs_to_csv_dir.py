#!/usr/bin/python3
'''
gtfs_to_csv_dir.py

Process all folders in unzipped directory
use multiprocessing module.

See gtfs_to_csv.py
'''

import os
from time import time
import argparse
import multiprocessing as mp
from local_modules.functions import date_path_concat
from gtfs_to_csv import get_gtfs_files, gtfs_to_df

def gtfs_dir_to_df(gtfs_dir, dataframes_dir):
    '''call gtfs_to_df on gtfs_files in gtfs_dir
    '''
    gtfs_files = get_gtfs_files(unzip_dir, gtfs_dir)
    realtime_date = (int(gtfs_dir[8:12]),
                     int(gtfs_dir[13:15]),
                     int(gtfs_dir[16:18]))
    target_dir = date_path_concat(*realtime_date)
    gtfs_to_df(gtfs_files, dataframes_dir, target_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir', help="path to dir contanining directories of unzipped\
            realtime data")
    args = parser.parse_args()
    unzip_dir = args.dir

    unzip_dir_list = sorted(os.listdir(unzip_dir))
    print(unzip_dir_list)
    dataframes_dir = os.path.dirname(args.dir)+'/'+'raw_frames'
    cores = mp.cpu_count()
    print(cores)
    pool = mp.Pool(cores)
    t = time()
    multiple_results = [
        pool.apply_async(gtfs_dir_to_df, (gtfs_dir, dataframes_dir))
        for gtfs_dir in unzip_dir_list]
    r = [res.get() for res in multiple_results]
    print(time() - t)

