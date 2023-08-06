import os
import json
import shutil
from crontab import CronTab


DEFAULT_CONF_FILE = os.path.join(os.path.dirname(__file__), 'CONFIG.JSON')
CONF_FILE = os.path.join(os.path.expanduser('~'), 'CONFIG.JSON')

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


def enable_w1():
    try:
        if os.geteuid() != 0:
            raise AttributeError
    except AttributeError:
        print('You need root privileges on a UNIX OS to run this command.\nRun again like:\nsudo python3 -m raspi_logger enable_w1')
        return

    # get the script location
    PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'enable_w1.sh'))

    # make it executeable
    os.chmod(PATH, 0o755)
    
    # we run with sudo
    cron = CronTab(user='root')
    job = cron.new(command='%s' % PATH)
    job.every_reboot()
    cron.write()

    print('OneWire enabled.')
