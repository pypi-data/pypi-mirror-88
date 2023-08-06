import click

from puddl import get_config
from puddl.apps import App


@click.group()
def app():
    pass


@app.command('add')
@click.argument('package_path')
def app_add(package_path):
    conf = get_config()
    conf.add_app(package_path)
    conf.write()


@app.command('ls')
@click.option('-v', '--verbose', is_flag=True)
def app_ls(verbose):
    conf = get_config()
    apps = sorted(conf['apps'])
    for app_name in apps:
        msg = app_name
        if verbose:
            msg = str(App(app_name))
        click.echo(msg)


@app.command('rm')
@click.argument('package_path')
def app_remove(package_path):
    conf = get_config()
    conf.remove_app(package_path)
    conf.write()
