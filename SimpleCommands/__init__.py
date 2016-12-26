import click
import logging
from SimpleCommands.DatabaseStatus import IsDatabaseHealthy

conn = None
db = None

def initModule(conn_, db_):
    global conn
    global db
    conn = conn_
    db = db_

@click.command()
def status():
    healthy = IsDatabaseHealthy(conn, db)
    click.echo('Database status:')
    if healthy:
        click.secho("Database is possibly ok", fg='green')
    else:
        click.secho("Something is wrong", fg='red')


@click.command()
def init():
    try:
        db.create_collection('sets')
        db.create_collection('files')
        db.create_collection('networks')
    except Exception as e:
        logging.getLogger('kalinka.init').error("Exception: {err}".format(err=e))
        click.secho("Database cannot be initialised", fg='red')
        return
    click.secho("Database sucessfully initialised", fg='green')
