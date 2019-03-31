'''
local_functions.py

module repository of functions used throught the application
'''

from datetime import date, timedelta

def date_path_concat(y, m, d):
    '''concat date tuple to 'y_m_d' format
    '''
    return str(y)+'_'+str(m).zfill(2)+'_'+str(d).zfill(2)

def date_to_int(y, m, d):
    '''return date tuple from string tuple
    '''
    return int(str(y)+str(m).zfill(2)+str(d).zfill(2))

def date_add_day(y, m, d, dif):
    '''return new date tuple from old date tuple + dif
    '''
    d = date(y, m, d)
    n = d + timedelta(days=dif)
    return (n.year, n.month, n.day)
