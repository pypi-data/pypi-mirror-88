import os
import json
from datetime import datetime as dt
from time import time, sleep
from crontab import CronTab

from .util import parse_interval_to_seconds, config, load_sensor, load_backend
from raspi_logger.backends.sqlite_backend import append_data as append_sqlite
from raspi_logger.backends.json_backend import append_data as append_json
# TODO: build a load_backend util, just like used with sensors


def current_data(sensor='all', dry=False, **kwargs):
    # get the config
    conf = config()

    # get the sensor modules
    sensorBackends = conf.get('sensorBackends', {'ds18b20': {}})

    # data buffer
    data = []
    for sen, sensor_conf in sensorBackends.items():
        if sensor == 'all' or sen.lower() == sensor.lower():
            # load the sensor_module:
            mod = load_sensor(sensor_name=sen)
            data.extend(mod.read_sensor(sensor_conf=sensor_conf, **kwargs))
    
    # in dry runs, only return the data
    if dry:
        return data

    if len(data) == 0:
        print('[ERROR]: recieved no data. Need better logging. Sorry.')
        return []
    
    # check the registered backends
    for name, c in conf.get('loggerBackends', {}).items():
        # check if the backend is currently enabled
        if c.get('enabled', True):
            if name == 'json':
                append_json(data, conf)
            elif name == 'sqlite':
                append_sqlite(data, conf)

    # return the data for reuse
    return data


def show_current_data(**kwargs):
    """
    Issue a new sensor reading, without saving.\n
    For reading new values **with** saving, use the 
    current_data function.
    """
    return current_data(dry=True, **kwargs)


def read_data(backend='json', limit=None, **kwargs):
    conf = config()
    bconf = conf.get('loggerBackends', {}).get(backend)

    if bconf is None:
        print("The '%s' seems to be disabled" % backend)
        return []
    
    # get the read function
    mod = load_backend(backend_name=backend)
    return mod.read_data(limit=limit, conf=conf, **kwargs)


def delete_data(backend='json', all=False, older_than=None):
    """
    """
    conf = config()
    bconf = conf.get('loggerBackends', {})
    
    if backend == 'all':
        for name in bconf.keys():
            delete_data(backend=name, all=all, older_than=older_than)
    else:
        bconf = bconf.get(backend)

    if bconf is None:
        print("The '%s' seems to be disabled" % backend)
        return []
    
    # get the read function
    mod = load_backend(backend_name=backend)
    print('Deleting....', end='')
    mod.delete(all=all, older_than=older_than, conf=conf)


def stream(interval=None, dry=False, **kwargs):
    # get the start time
    t1 = time()
    
    if interval is None:
        interval = config().get('loggerInterval', '1min')
    else:
        config(loggerInterval=interval)
    
    if isinstance(interval, str):
        interval = parse_interval_to_seconds(interval)
    
    data = current_data(dry=dry, **kwargs)

    # stringify
    outstr = json.dumps(data, indent=4)

    # print
    print(outstr)

    # sleep for the remaining time
    remain = interval - (time() - t1)
    if remain < 0:
        remain = 0
    sleep(remain)

    # call again
    stream(dry=dry, **kwargs)
