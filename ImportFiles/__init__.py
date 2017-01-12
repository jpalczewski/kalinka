import click
from multiprocessing import Pool
from pathlib import Path
import hashlib
from collections import Counter, defaultdict

conn = None
db = None
config = None
files_collection = None

allowed_filetypes = ['py', 'cpp', 'c', 'java', 'hpp', 'hxx', 'h', 'php', 'php']
language_lookup_table = {
    'py': 'Python',
    'cpp': 'C++',
    'c':'C',
    'cs':'C#',
    'java':'Java',
    'hpp':'C++',
    'hxx':'C++',
    'h':'C',
    'php':"PHP"

}
def importInit(conn_, db_, config_):
    global conn
    global db
    global config
    global files_collection

    conn = conn_
    db = db_
    config = config_
    files_collection = db['files']

@click.group(name='import', help="Group of files about importing files")
def import_group():
    pass


@click.command(name='full', help="Performs full import(three-step pass)")
def import_full():
    global files_collection
    def addFile(f, hash):
        global files_collection
        content = None
        ext = f.parts[2]
        with f.open() as fh:
            try:
                content = fh.read()
                files_collection.insert_one({'filetype':ext, 'content':content,'language':language_lookup_table[ext], 'hash':hash, 'stats':{'simple':{}}})
            except Exception as e:
                click.secho("ERROR: {0}".format(e), fg='red')
    def countAscii(f, hash):
        pass
    #remove everything
    files_collection.remove({})
    #files_collection.create_index()
       #lets rock
    data_directory = config['server']['data']
    path = Path(data_directory)
    allFiles = list(path.glob('*/*'))
    ReviewAllFilesOnDisk(allFiles, addFile)
    ReviewAllFilesOnDisk(allFiles, CountSimpleStats)


import_group.add_command(import_full)



def ReviewAllFilesOnDisk(files, func):
    print("!")
    reviewedFiles = set()
    skippedFiles = 0
    for f in files:
        ext = f.parts[2]
        if ext in allowed_filetypes:
            with f.open('rb') as fh:
                try:
                    hash = hashfile(fh, hashlib.md5())
                except:
                    continue
            if hash in reviewedFiles:
                skippedFiles = skippedFiles + 1
                continue
            reviewedFiles.add(hash)
            try:
                func(f,hash)
            except:
                continue

#http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

def CountSimpleStats(file, hash):
    ascii_count = defaultdict(int)
    ascii_count_per_line = []
    with file.open() as fh:
        for line in fh:
            ascii_count_per_line.append(defaultdict(int))
            for char in line:
                if char == '.':
                    char = 'dot'
                elif char == '$':
                    char = 'dollar'
                elif char == "\0":
                    char = "null"
                ascii_count[char] = ascii_count[char] + 1
                ascii_count_per_line[-1][char] = ascii_count_per_line[-1][char] + 1
            sumOfOccurences = sum(ascii_count_per_line[-1].values())
            for key, value in ascii_count_per_line[-1].items():
                ascii_count_per_line[-1][key] = value/sumOfOccurences
        sumOfOccurences = sum(ascii_count.values())
    for key, value in ascii_count.items():
        ascii_count[key] = value / sumOfOccurences
    files_collection.update_one({'hash':hash}, {"$set":{'stats':{'simple':{'ascii_count':ascii_count, 'ascii_count_per_line':ascii_count_per_line}}}}
        #db.files.updateOne({hash:'3fecd45b11216e1c9f9a53bcf9810ec9'},{ $set: {stats:{simple:{ascii:{'a':2}}}}})
    )