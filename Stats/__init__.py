import click
from SimpleCommands.DatabaseHealth import IsDatabaseHealthy
from Stats.StatsUtils import ExecuteForAllFiles
from collections import Counter
conn = None
db = None
def statsInit(conn_, db_):
    global conn
    global db
    conn = conn_
    db = db_

@click.group(help='Group related with calculating statistics in database')
def stats():
    pass


@click.group(help='Group of time-consuming function.')
def generate():
    pass


@click.command(help="Clean 'stats' key in all files")
def clean():

    if not IsDatabaseHealthy(conn, db):
        click.secho("Don't do it.", fg='red')

    ExecuteForAllFiles(db, removeStats)

@click.command(help='Calculate "simple" statistics')
def simple():
    if not IsDatabaseHealthy(conn, db):
        click.secho("Don't do it.", fg='red')

    ExecuteForAllFiles(db, generateSimple)

stats.add_command(clean)
stats.add_command(generate)
generate.add_command(simple)

def generateSimple(f):
    cleaned = f['content'].replace("\0", "")
    c_char = dict(Counter(cleaned).items())
    #c_tokens = dict(Counter(cleaned.split()).items())
    c_ascii = {}
    clearToASCII(c_ascii, c_char)

    lines = cleaned.split("\n")
   # lines = [clearToASCII({}, dict(Counter(x).items())) for x in lines]

    if 'stats' not in f:
        f['stats'] = {}
    f['stats']['simple'] = {'ascii':c_ascii, 'ascii_per_lines':lines}
    return f


def clearToASCII(c_ascii, c_char):
    for k in c_char:
        if ord(k) < 128:
            c_ascii[k] = c_char[k]
    if '.' in c_ascii:
        c_ascii['dot'] = c_ascii.pop('.')
    if '$' in c_ascii:
        c_ascii['dollar'] = c_ascii.pop('$')

    return c_ascii


def removeStats(f):
    f.pop('stats', None)
    return f
