import click
from SimpleCommands.DatabaseHealth import IsDatabaseHealthy
from Stats.StatsUtils import ExecuteForAllFiles
conn = None
db = None
def statsInit(conn_, db_):
    global conn
    global db
    conn = conn_
    db = db_

@click.group()
def stats():
    pass


@click.command(help="Clean 'stats' key in all files")
def clean():

    if not IsDatabaseHealthy(conn, db):
        click.secho("Don't do it.", fg='red')


    click.secho("Warning: don't use that db during that operation, because all files are reinserted", fg='yellow')

    ExecuteForAllFiles(db, removeStats)



stats.add_command(clean)


def removeStats(f):
    f.pop('stats', None)
    return f
