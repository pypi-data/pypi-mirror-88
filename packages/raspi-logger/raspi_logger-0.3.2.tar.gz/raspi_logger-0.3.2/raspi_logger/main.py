from crontab import CronTab

from .util import config, parse_interval_to_seconds, reset_config
from .logger import current_data


# maybe activate a a sensor protocol directly? for multiple cronjobs?
def activate(sensor='all', basecmd='python3 -m raspi_logger run'):
    # get the sensor backends
    conf = config()
    sensorBackends = conf.get('sensorBackends')

    # get the sensors to be activated
    if sensor == 'all':
        sensors = sensor.Backends.keys()
    else:
        sensors = [sensor]
    
    for sen in sensors:
        cmd = '%s --sensor=%s' % (basecmd, sen)
        __activate(cmt=sen, basecmd=cmd, conf=conf)
    

def __activate(sensor_name, basecmd, conf):
    # get the interval setting
    _interval = conf['sensorBackends'][sensor_name].get('interval')
    if _interval is None:
        _interval = conf.get('loggerInterval', '15min')
    
    # parse
    interval = parse_interval_to_seconds(_interval)
    
    # determine cronjob settings
    if interval < 60:
        # less than a minute is not supported by crontab
        seconds = list(range(0, 60, interval))

        # get the crontab
        cron = CronTab(user=True)
        cmds = ['sleep %d;%s' % (s, basecmd) for s in seconds]
        jobs = [cron.new(command=cmd, comment=cmt) for cmd in cmds]
        for job in jobs:
            job.minute.every(1)
    else:
        cron = CronTab(user=True)
        job = cron.new(command=basecmd, comment=cmt)
        job.minute.every(int(interval / 60))
    
    # save 
    cron.write()

    # change config
    config(loggerCronjob='enabled')
    print('Saved.')


def deactivate(sensor='all'):
    # get the sensor backends
    conf = config()
    sensorBackends = conf.get('sensorBackends')

    # get the sensors to be activated
    if sensor == 'all':
        sensors = sensorBackends.keys()
    else:
        sensors = [sensor]
    
    for sen in sensors:
        __deactivate(comment=sen)


def __deactivate(comment):
    # disable the config first
    config(loggerCronjob='disabled')

    # get the crontab
    cron = CronTab(user=True)
    jobs = list(cron.find_comment(comment))

    # delete all
    for job in jobs:
        job.delete()
    
    cron.write()
    print('Stopped.')


def run():
    # first check if we should still log:
    conf = config()
    if conf.get('loggerCronjob', 'disabled')=='disabled':
        deactivate()
        return 

    # do the logging - TODO: here we could add a logic to handle more sensors
    current_data()


def settings(interval=None, enable=None, disable=None, enable_backend=None, disable_backend=None, reset=False):
    """
    Raspi Logger Settings\n
    Change the settings of the logger firmware, while the logger is running. 
    There is no need to shut the logger down. 
    Use this API for an IoT interface.
    :param interval: string - set a new measuring interval. E.g: '15min' or '4hrs'
        Using less than a Minute is experimental. Using less than 10sec can 
        cause the logger to crash with JSON backend.
    :param enable: If set, the logger will be activated. See activate command
    :param disable: IF set, the logger will be deactivated. See deactivate command
    :param enable_backend: string - Set the storage backend name to be enabed.
        Currenty a JSON file ('json') or a local sqlite DB ('sqlite') are supported.
    :param disable_backend: string - see enable_backend
    :param reset: If set, the config file will be completely reset.
        If you pass the reset flag along with other flags, these changes will be
        applied **after** the reset. 
    """
    if reset:
        reset_config()

    # check the settings
    # set new Interval
    if interval is not None:
        # delete the old activation
        deactivate()

        # TODO: validate the settings before writing
        config(loggerInterval=interval)

        # activate again
        activate()

    # activate or deactivate the logger
    if isinstance(enable, bool) and enable:
        activate()
    if isinstance(disable, bool) and disable:
        deactivate()

    # check if a storage backend should be enabled
    backends = config().get('loggerBackends')
    if enable_backend is not None:
        backends[enable_backend]['enabled'] = True
    if disable_backend is not None:
        backends[disable_backend]['enabled'] = False
    config(loggerBackends=backends)

    return config()
    