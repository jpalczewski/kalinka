from multiprocessing import Pool,cpu_count
import click

def ExecuteForAllFiles(db, func):
    click.secho("Warning: don't use that db during that operation, because all files are reinserted", fg='yellow')
    files = db.files
    allFiles = list(files.find({}))
    results = None

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(func, allFiles)

    files.remove({})
    files.insert_many(results, ordered=False)
