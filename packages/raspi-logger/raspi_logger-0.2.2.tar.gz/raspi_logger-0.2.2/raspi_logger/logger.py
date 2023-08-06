import os
import json
from datetime import datetime as dt
from time import time, sleep
from crontab import CronTab

from .util import parse_interval_to_seconds, config, load_sensor
from raspi_logger.backends.sqlite_backend import append_data as append_sqlite
from raspi_logger.backends.json_backend import append_data as append_json
# TODO: build a load_backend util, just like used with sensors


def save_data(path=None, dry=False, **kwargs):
    # get the config
    conf = config()

    # get the sensor modules
    sensors = conf.get('sensor_modules', ['ds18b20'])

    # data buffer
    data = []
    for sensor in sensors:
        # load the sensor_module:
        mod = load_sensor(sensor_name=sensor)
        data.extend(mod.read_sensor(conf=conf, **kwargs))
    
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
                append_json(data, conf, path)
            elif name == 'sqlite':
                append_json(data, conf, path)

    # return the data for reuse
    return data


def stream(interval=None, dry=False, **kwargs):
    # get the start time
    t1 = time()
    
    if interval is None:
        interval = config().get('loggerInterval', '1min')
    else:
        config(loggerInterval=interval)
    
    if isinstance(interval, str):
        interval = parse_interval_to_seconds(interval)
    
    data = save_data(dry=dry, **kwargs)

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
