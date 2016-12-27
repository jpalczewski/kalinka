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
    c_ascii = Counter((c for c in splitascii_iter(f['content'])))
 #   c_lines = (Counter(c) for c in splitnewlines_iter(f['content']))

    c_ascii = removeDotsAndDollars(c_ascii)
#    c_lines = (removeDotsAndDollars(d) for d in c_lines)
#   'ascii_per_lines':list(c_lines)
    if 'stats' not in f:
        f['stats'] = {}
    f['stats']['simple'] = {'ascii':c_ascii}
    return f


def splitnewlines_iter(string):
    return (x.group(0) for x in re.finditer(r".*\n|.+$", string))

def splitascii_iter(string):
    for c in string:
        if ord(c) < 128 and ord(c) > 0:
            yield c

def removeDotsAndDollars(d):
    if '$' in d:
        d['dollar'] = d.pop('$')
    if '.' in d:
        d['dot'] = d.pop('.')
    return d
def removeStats(f):
    f.pop('stats', None)
    return f
