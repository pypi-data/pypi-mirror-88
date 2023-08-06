import os
import json
import shutil
from importlib import import_module
from crontab import CronTab


DEFAULT_CONF_FILE = os.path.join(os.path.dirname(__file__), 'CONFIG.JSON')
CONF_FILE = os.path.join(os.path.expanduser('~'), 'CONFIG.JSON')

ENABLE_W1_TEMPLATE="""
#!/bin/sh -e
#
# Start One Wire protocol
#
# You need sudo to run this script. 
# 
# This script should be called in /etc/rc.local to be run
# on each system startup. Alternatively, define a cronjob:
#
# >> sudo crontab -e
# >> @reboot /path/to/enable_w1.sh
#

{commands}
exit 0
"""


def get_serial_number():
    # dummy versions
    versions = dict(
        hardware='xxxxxxx',
        revision='0000000',
        serial='0000000000000000'
    )

    # open cpu info and read
    try:
        with open('/proc/cpuinfo', 'r') as info:
            for line in info:
                if line.startswith('Hardware'):
                    versions['hardware'] = line.split(':')[1].strip()
                elif line.startswith('Revision'):
                    versions['revision'] = line.split(':')[1].strip()
                elif line.startswith('Serial'):
                    versions['serial'] = line.split(':')[1].strip()

    except:
        versions = dict(
        hardware='ERRORxx',
        revision='ERROR00',
        serial='ERROR00000000000'
    )

    return versions


def parse_interval_to_seconds(s: str) -> int:
    s = s.lower()

    # Hours
    if 'hrs' in s:
        s = s.replace('hrs', 'h')
    if 'h' in s:
        s = s.replace('h', '')
        t = int(s)
        return t * 3600
    
    # Minutes
    if 'min' in s:
        s = s.replace('min', 'm')
    if 'm' in s:
        s = s.replace('m', '')
        t = int(s)
        return t * 60

    # Seconds
    if 'sec' in s:
        s = s.replace('sec', 's')
    if 's' in s:
        s = s.replace('s', '')
        return int(s)


def load_sensor(sensor_name: str):
    # try to load the module from raspi_logger.sensors
    try:
        return import_module('raspi_logger.sensors.%s' % sensor_name)
    except AttributeError:
        pass
    
    # if still here, load from globals
    if sensor_name in globals():
        return globals()[sensor_name]
    else:
        raise ValueError("A sensor of name '%s' could not be loaded." % sensor_name)


def load_backend(backend_name: str):
    # try to load the module from raspi_logger.backends
    try:
        return import_module('raspi_logger.backends.%s_backend' % backend_name)
    except AttributeError:
        pass

    # if still here, load from globals
    if backend_name in globals():
        return globals()[backend_name]
    else:
        raise ValueError("A backend of name '%s' could not be loaded." % backend_name)


def config(**kwargs) -> dict:
    if not os.path.exists(CONF_FILE):
        shutil.copy(DEFAULT_CONF_FILE, CONF_FILE)
    
    # get the config
    with open(CONF_FILE, 'r') as f:
        conf = json.load(f)

    # check if we are in read or write mode
    if len(kwargs.keys()) == 0:
        return conf 
    else:
        conf.update(kwargs)

        # write
        with open(CONF_FILE, 'w') as f:
            json.dump(conf, f, indent=4)
        
        return conf


def reset_config():
    shutil.copy(DEFAULT_CONF_FILE, CONF_FILE)


def enable_w1(path=None, gpio=[4]):
    TEMPLATE = '# enable w1 on GPIO {pin}\ndtoverlay w1-gpio gpiopin={pin} pullup=0'
    try:
        if os.geteuid() != 0:
            raise AttributeError
    except AttributeError:
        print('You need root privileges on a UNIX OS to run this command.\nRun again like:\nsudo python3 -m raspi_logger enable_w1')
        return

    # get the script location
    if path is None:
        PATH = os.path.abspath(os.path.join(os.path.expanduser('~'), 'enable_w1.sh'))
    else:
        PATH = path

    # create the script
    cmds = '\n'.join([TEMPLATE.format(pin=pin) for pin in gpio])
    # copth the file over
    with open(PATH, 'w') as shellscript:
        shellscript.write(ENABLE_W1_TEMPLATE.format(commands=cmds))

    # make it executeable
    os.chmod(PATH, 0o755)
    
    # we run with sudo
    cron = CronTab(user='root')
    job = cron.new(command='%s' % PATH)
    job.every_reboot()
    cron.write()

    print('OneWire enabled. GPIO: %s' % (', '.join([str(pin) for pin in gpio])))
