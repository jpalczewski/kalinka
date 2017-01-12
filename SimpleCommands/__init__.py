import click
import logging
from SimpleCommands.DatabaseHealth import IsDatabaseHealthy
from plotly.offline import plot
conn = None
db = None

def simpleInit(conn_, db_):
    global conn
    global db
    conn = conn_
    db = db_

@click.command(help="Check if database is healthy.")
def health():
    healthy = IsDatabaseHealthy(conn, db, False)
    click.echo('Database status:')
    if healthy:
        click.secho("Database is possibly ok", fg='green')
    else:
        click.secho("Something is wrong", fg='red')


@click.command(help="Initialize database.")
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



@click.command(help="Print count of files, networks and sets")
def status():
    if not IsDatabaseHealthy(conn, db):
        click.secho("I won't tell anything because database is invalid.", fg='red')
        return

    print("Number of records:")
    for collection in db.collection_names():
        print(collection,"\t\t", db[collection].find({}).count())


@click.command(help="Show what kind of files are available in files collection.")
@click.option('--plotly/--no-plotly', default=False, help="Generates html graph")
def languages(plotly):
    if not IsDatabaseHealthy(conn, db):
        click.secho("I won't tell anything because database is invalid.", fg='red')
        return
    logger = logging.getLogger('kalinka.languages')
    files = db.files
    allLanguages = files.distinct("filetype")
    numOfFiles = {}

    logger.debug("allLanguages: %s", allLanguages)
    for l in allLanguages:
        numOfFiles[l] = files.find({'language':l}).count()

    if(plotly):
        plot({
            'data': [{'labels': list(numOfFiles.keys()), 'values': list(numOfFiles.values()), 'type': 'pie'}]
        })