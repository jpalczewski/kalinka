"""Main app."""
import click
import configparser
import logging
import pymongo
import sys


import ImportFiles
import SimpleCommands
import Stats

motd = """
  _         _ _       _
 | | ____ _| (_)_ __ | | ____ _
 | |/ / _` | | | '_ \| |/ / _` |
 |   < (_| | | | | | |   < (_| |
 |_|\_\__,_|_|_|_| |_|_|\_\__,_|
 """

conn = []
config = []
db = []


@click.group()
@click.option('--info', 'level', flag_value=1, default=True,
              help="Shows only info messages")
@click.option('--debug', 'level', flag_value=2,
              help="Shows debug messages")
@click.option('--quiet', 'level', flag_value=0,
              help="Only error messages.")
def cli(level):
    levels = [logging.ERROR, logging.INFO, logging.DEBUG]
    ch.setLevel(levels[level])
    logger.setLevel(levels[level])


# Defining whole structure
cli.add_command(SimpleCommands.health)
cli.add_command(SimpleCommands.init)
cli.add_command(SimpleCommands.status)
cli.add_command(SimpleCommands.languages)
#cli.add_command(Stats.stats)
cli.add_command(ImportFiles.import_group)

logger = logging.getLogger('kalinka')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        conn = pymongo.MongoClient(
            config['server']['host'],
            int(config['server']['port']),
            serverSelectionTimeoutMS=2000,
            connect=False)
        db = conn[config['server']['database']]
        SimpleCommands.simpleInit(conn, db)
        Stats.statsInit(conn, db)
        ImportFiles.importInit(conn, db, config)
    except Exception as e:
        logger.critical(
            "Database or config file exception:{err}".format(err=e)
        )
        sys.exit(1)

    click.secho(motd, fg='green')
    cli()
