import sys
import click

from loguru import logger

from src.core.Config import Config
from src.commands.SyncKohaRowsCommand import SyncKohaRowsCommand
from src.commands.LoadConfigFileCommand import LoadConfigFileCommand
from src.commands.ValidateApiCommand import ValidateApiCommand
from src.commands.ValidateKohaDBCommand import ValidateKohaDBCommand


koha_sync_version = '1.2.0'


@click.command()
@click.option('-c', '--config-file', 'config_file', required=True, help="path to config file [db] or [Koha_api]")
@click.option('-v', '--verbose', 'verbosity', count=True, help="activate verbosity output")
@click.option('-V', '--version', 'version', is_flag=True, help="print current cli version and stops execution")
@click.option('-r', '--run-once', 'run_once', is_flag=True, help="synchronize once and stops execution")
@click.option('-t', '--test', 'test', is_flag=True, help="run validations and stops before synchronize")
def main(config_file, verbosity, run_once, test, version):
    # click.secho('Hello {0} {1} {3} {2}'.format(config_file, verbosity, test, run_once))
    # click.secho(f'Hello {config_file} {verbosity} {run_once} {test}')
    if version:
        sys.exit(logger.success(f"you are running {koha_sync_version} version"))

    # verify and load configuration file
    LoadConfigFileCommand(file_path=config_file).execute()

    # validate API availability
    ValidateApiCommand().execute()

    # validate Koha DB availability
    if Config.source == 'db':
        ValidateKohaDBCommand().execute()

    # synchronize koha registries
    while True:

        if test:
            logger.info("STOPPING EXCECUTION BECAUSE OF TEST FLAG !")
            break

        SyncKohaRowsCommand().execute()

        if run_once:
            logger.info("STOPPING EXCECUTION BECAUSE OF RUN ONCE FLAG !")
            break


# @click.command()
# @click.option('--count', default=1, help='number of greetings')
# @click.argument('name')
# def hello(count, name):

# @click.option('--count', default=1, help='number of greetings')
# @click.argument('name')
# @click.command()
# def init_db():
#     click.echo('initialized the db')

# @cli.command()
# def perform_query():
#     click.echo('querying ...')

# @click.command()
# def drop_db():
#     click.echo('dropped the db')

# cli.add_command(init_db)
# cli.add_command(drop_db)
# cli.add_command(hello)
