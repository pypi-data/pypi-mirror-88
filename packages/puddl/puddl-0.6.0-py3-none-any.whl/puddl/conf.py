import json
import logging
import os
from collections import UserDict
from pathlib import Path
from urllib.parse import urlencode

from puddl.apps import App

log = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class Config(UserDict):
    PUDDLRC = Path.home() / '.puddlrc'

    DB_DEFAULTS = {
        'PGUSER': os.environ.get('PGUSER'),
        'PGPASSWORD': os.environ.get('PGPASSWORD'),
        'PGHOST': os.environ.get('PGHOST'),
        'PGPORT': os.environ.get('PGPORT'),
        'PGDATABASE': os.environ.get('PGDATABASE'),
        'PGAPPNAME': os.environ.get('PGAPPNAME', 'puddl'),
    }

    @classmethod
    def get_defaults(cls):
        defaults = cls.DB_DEFAULTS.copy()
        defaults['apps'] = []
        return defaults

    def write(self):
        x = json.dumps(self.data, indent=2, sort_keys=True)
        with self.PUDDLRC.open('w') as f:
            f.write(x)

    @property
    def apps(self):
        return self['apps']

    @property
    def db_url(self) -> str:
        db_params = {
            'application_name': self['PGAPPNAME']
        }
        return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}' \
               '/{PGDATABASE}?{params}'.format(**self, params=urlencode(db_params))

    @property
    def db_env(self):
        return {k: v for k, v in self.items() if k in self.DB_DEFAULTS.keys()}

    def add_app(self, name):
        p = App(name)
        p.validate()
        self['apps'].append(p.pkg_name)

    def remove_app(self, name):
        ps = self['apps']
        try:
            del ps[ps.index(name)]
        except ValueError:
            log.warning(f'app {name} was not installed')

    def get_app_from_module_name(self, module: str):
        """
        Given `puddl.felix.codimd.cli` return `puddl.felix.codimd` if `puddl.felix.codimd`
        is installed.
        """
        for installed_app_name in self['apps']:
            if module.startswith(installed_app_name):
                return App(installed_app_name)
        return None


class DBConfig:
    """
    Abstracts a subset of the libpq environment variables defined by
    https://www.postgresql.org/docs/current/libpq-envars.html

    >>> puddl_root_db_config = DBConfig()
    >>> puddl_root_db_config.url
    'postgresql://puddl:aey1Ki4oaZohseWod2ri@localhost:13370/puddl?application_name=puddl'

    Given an app name, user and password are set accordingly

    >>> app_db_config = DBConfig('foo')
    >>> app_db_config.url
    'postgresql://foo:foo-aey1Ki4oaZohseWod2ri@localhost:13370/puddl?application_name=foo'
    """
    __slots__ = ['PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT', 'PGDATABASE', 'PGAPPNAME']

    def __init__(self, name=None):
        env_vars_missing = []
        for key in self.__slots__:
            try:
                setattr(self, key, os.environ[key])
            except KeyError as e:
                key = e.args[0]
                env_vars_missing.append(key)

        conf_vars_missing = []
        if env_vars_missing:
            conf = get_config()
            for key in env_vars_missing:
                try:
                    value = conf[key]
                    setattr(self, key, value)
                except KeyError:
                    conf_vars_missing.append(key)

        if conf_vars_missing:
            raise ConfigError(f'Missing variables: {env_vars_missing}. You may set them '
                              f'in the environment or by initializing ~/.puddlrc')
        if name is not None:
            self.PGUSER = name
            self.PGPASSWORD = '-'.join((name, self.PGPASSWORD))
            self.PGAPPNAME = name

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    @property
    def url(self) -> str:
        db_params = {
            'application_name': self.PGAPPNAME
        }
        params = urlencode(db_params)
        return f'postgresql://{self.PGUSER}:{self.PGPASSWORD}' \
               f'@{self.PGHOST}:{self.PGPORT}' \
               f'/{self.PGDATABASE}?{params}'

    def __str__(self):
        return self.PGUSER

    def __repr__(self):
        return f"DBConfig('{self.PGUSER}')"


def get_config(app=None):
    try:
        with Config.PUDDLRC.open() as f:
            data = json.load(f)
    except FileNotFoundError:
        data = Config.get_defaults()
    except json.decoder.JSONDecodeError as e:
        raise ConfigError(
            f'{Config.PUDDLRC}:{e.lineno} column {e.colno} char {e.pos}: {e.msg}'
        )
    cfg = Config(**data)
    # app must be one of the installed apps
    if app is None:
        app = 'puddl'

    data['PGAPPNAME'] = app
    return cfg
