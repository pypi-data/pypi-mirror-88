import logging
from pathlib import Path

import click

from puddl.conf import Config, get_config

log = logging.getLogger(__name__)


@click.group()
def config():
    pass


@config.command()
def init():
    data = {}
    defaults = Config.get_defaults()
    data.update(defaults)

    dot_env = Path('.env')
    try:
        with dot_env.open() as f:
            contents = f.read()
        for line in contents.strip().split('\n'):
            k, v = line.strip().split('=')
            if k in defaults:
                log.info(f'using {k} from .env')
                data[k] = v
    except FileNotFoundError:
        pass

    conf = Config(data)
    conf.write()


@config.command()
def show():
    conf = get_config()
    print(conf.data)
