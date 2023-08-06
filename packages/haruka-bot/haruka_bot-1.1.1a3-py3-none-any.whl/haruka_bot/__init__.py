import nonebot

try:
    nonebot.get_driver()
    from . import config_manager
    from . import live_pusher
    from . import dynamic_pusher
    from . import auto_agree
except ValueError:
    from . import cli

from .version import __version__
