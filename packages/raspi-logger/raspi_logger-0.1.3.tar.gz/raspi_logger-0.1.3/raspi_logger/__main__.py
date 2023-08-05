import fire

from .main import run, activate, deactivate, settings
from .logger import stream
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
    'enable_w1': enable_w1
})
