import os
import json
from os.path import join as pjoin
from datetime import datetime as dt


def append_data(new_data, conf, path=None):
    """
    path is deprecated and will be removed. The file path has to be specified
    in the CONFIG file.
    """
    # set path to None
    path = None
    # create a new file per day
    if path is None:
        date = dt.now().date()
        fname = '%d_%d_%d_raw_log.json' % (date.year, date.month, date.day)

        # get path
        path = pjoin(conf.get('loggerPath', pjoin(os.path.expanduser('~'), 'logger')), fname)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

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
