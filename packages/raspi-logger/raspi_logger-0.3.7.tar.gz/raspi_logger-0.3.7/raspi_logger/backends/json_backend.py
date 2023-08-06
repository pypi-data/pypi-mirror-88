import os
import json
import glob
from os.path import join as pjoin
from datetime import datetime as dt

from raspi_logger.util import config

def append_data(new_data, conf):
    """
    path is deprecated and will be removed. The file path has to be specified
    in the CONFIG file.
    """
    # get the path
    date = dt.now().date()
    fname = '%d_%d_%d_raw_log.json' % (date.year, date.month, date.day)

    # get path
    # TODO: depreacte conf as argument and read the config file
    path = conf.get('loggerPath', pjoin(os.path.expanduser('~'), 'logger'))

    if not os.path.exists(path):
        os.makedirs(path)
        config(loggerPath=path)
    
    # get the filename path
    path = pjoin(path, fname)

    # save data
    # get existing data
    try:
        with open(path, 'r') as f:
            old_data = json.load(f)
    except:
        old_data = []
    
    # append and save
    with open(path, 'w') as js:
        old_data.extend(new_data)
        json.dump(old_data, js, indent=4)


def read_data(limit=None, max_files=None, **kwargs):
    """
    
    """
    # read the config
    conf = config()

    if not 'loggerPath' in conf:
        print('[ERROR]: No data saved as JSON.')
        return []

    # get the file path
    path = conf['loggerPath']

    # get all files
    data_files = glob.glob(pjoin(path, '*.json'))
    
    # sort - latest one as **first** element
    data_files.sort(key=os.path.getctime, reverse=True)

    # limit the maximum number of files to be read
    if max_files is not None:
        end_at = max_files if max_files < len(data_files) else len(data_files) 
        data_files = data_files[:end_at]

    # read the data
    sorter = lambda c: dt.fromisoformat(c['tstamp']).timestamp()
    data = []
    for fname in data_files:
        # load file content
        with open(fname, 'r') as f:
            data = json.load(f) + data
        
        # check if we have enough
        if limit is None:
            continue
        elif len(data) > limit:
            # we have enough data
            data.sort(key=sorter, reverse=True)
            return data[:limit][::-1]
    
    # if we reach this line, there was less data than limit or no limit
    data.sort(key=sorter)
    return data
