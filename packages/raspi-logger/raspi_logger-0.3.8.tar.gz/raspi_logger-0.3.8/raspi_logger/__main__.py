import fire

from .main import run, activate, deactivate, settings
from .logger import stream, show_current_data, read_data, delete_data
from .util import enable_w1


fire.Fire({
    'run': run,
    'log': run,
    'settings': settings,
    'activate': activate,
    'start': activate,
    'deactivate': deactivate,
    'stop': deactivate,
    'stream': stream,
    'read-sensors': show_current_data,
    'read-data': read_data,
    'read': read_data,
    'delete-data': delete_data,
    'delete': delete_data,
    'enable_w1': enable_w1
})
