import fire

from .main import run, activate, deactivate, settings
from .logger import stream


fire.Fire({
    'run': run,
    'log': run,
    'settings': settings,
    'activate': activate,
    'start': activate,
    'deactivate': deactivate,
    'stop': deactivate,
    'stream': stream
})
