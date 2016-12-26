from multiprocessing import Pool,cpu_count

def ExecuteForAllFiles(db, func):
    files = db.files
    allFiles = list(files.find({}))
    results = None

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(func, allFiles)

    files.remove({})
    files.insert_many(results, ordered=False)
