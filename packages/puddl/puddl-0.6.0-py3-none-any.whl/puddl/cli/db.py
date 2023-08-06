import logging
import subprocess

import click

from puddl import get_config
from puddl.conf import DBConfig

log = logging.getLogger(__name__)


@click.group()
def db():
    pass


@db.command()
@click.option('--app')
def health(app):
    conf = DBConfig(app)

    import psycopg2
    # consumes PG* env vars
    connection = psycopg2.connect(conf.url)
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    log.info('database available')


@db.command()
@click.option('--app')
def shell(app):
    conf = DBConfig(app)
    conf.PGAPPNAME = 'puddl db shell'
    # want to see good error handling for this kind of thing?
    # https://github.com/pallets/click/blob/19fdc8509a1b946c088512e0e5e388a8d012f0ce/src/click/_termui_impl.py#L472-L487
    subprocess.Popen('psql', env=conf.to_dict()).wait()


@db.command()
@click.option('--app')
def url(app):
    """
    print DB URL

    Useful for things like this:

        from sqlalchemy import create_engine
        database_url = 'postgresql://puddl:aey1Ki4oaZohseWod2ri@localhost:13370/puddl'
        engine = create_engine(database_url, echo=False)
        df.to_sql('bp', engine)
    """
    conf = DBConfig(app)
    print(conf.url)


@db.command()
@click.option('--app')
def env(app):
    """
    Prints the database's environment.
    WARNING: This dumps your password. Use it like this:

        source <(puddl db env)
    """
    conf = DBConfig(app)
    for k, v in conf.to_dict().items():
        print(f'export {k}={v}')


@db.command()
def sessions():
    """
    Lists active sessions.
    """
    conf = get_config(app='db sessions')
    query = """SELECT pid AS process_id,
           usename AS username,
           datname AS database_name,
           client_addr AS client_address,
           application_name,
           backend_start,
           state,
           state_change
    FROM pg_stat_activity;"""
    click.echo(
        subprocess.check_output(['psql', '-c', query], encoding='utf-8', env=conf.db_env))
