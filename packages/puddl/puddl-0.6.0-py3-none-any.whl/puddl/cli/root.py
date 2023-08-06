import logging

import click

import puddl
from puddl.apps import App
from puddl.conf import get_config

log = logging.getLogger(__name__)
LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']


class AppsGroup(click.Group):

    def __init__(self, name=None, commands=None, **attrs):
        self._apps = [App(x) for x in get_config().apps]
        self._name2app = {
            x.cmd_name: x for x in self._apps
        }
        super().__init__(name, commands, **attrs)

    def list_commands(self, ctx):
        core_commands = set(super().list_commands(ctx))
        app_names = set(x for x in self._name2app)
        return sorted(core_commands | app_names)

    def get_command(self, ctx, cmd_name):
        if cmd_name in self._name2app:
            app = self._name2app[cmd_name]
            return app.get_command()
        return super().get_command(ctx, cmd_name)


@click.group(cls=AppsGroup)
@click.option('-l', '--log-level',
              type=click.Choice(LOG_LEVELS, case_sensitive=False),
              default='WARNING')
@click.option('-d', '--debug', is_flag=True,
              help='sets log level to DEBUG. ignores "--log-level"')
@click.option('--loggers', default='', help='comma-separated logger names')
@click.version_option(version=puddl.__version__)
def root(log_level, debug, loggers):
    if debug:
        log_level = 'DEBUG'
    logging.basicConfig(level=log_level)
    if loggers:
        for name in loggers.split(','):
            logging.getLogger(name).setLevel(log_level)
    pass
