# kalinka

Part of PSZT-16Z project - main idea of this script is 
automation of all necessary tasks with database, f.e.:
 - Inits database
 - Checks if everything works(f.e. if database is running)
 - Shows info about database state - files inside, etc.
 - And more!(_but it isn't implemented yet_)

## Usage

```bazaar

$ python kalinka.py
  _         _ _       _
 | | ____ _| (_)_ __ | | ____ _
 | |/ / _` | | | '_ \| |/ / _` |
 |   < (_| | | | | | |   < (_| |
 |_|\_\__,_|_|_|_| |_|_|\_\__,_|
 
Usage: kalinka.py [OPTIONS] COMMAND [ARGS]...

Options:
  --info   Shows only info messages
  --debug  Shows debug messages
  --quiet  Only error messages.
  --help   Show this message and exit.

Commands:
  health     Check if database is healthy.
  init       Initialize database.
  languages  Show what kind of files are available in...
  stats      Group related with calculating statistics in...
  status     Print count of files, networks and sets

```

```

$ python kalinka.py stats
  _         _ _       _
 | | ____ _| (_)_ __ | | ____ _
 | |/ / _` | | | '_ \| |/ / _` |
 |   < (_| | | | | | |   < (_| |
 |_|\_\__,_|_|_|_| |_|_|\_\__,_|
 
Usage: kalinka.py stats [OPTIONS] COMMAND [ARGS]...

  Group related with calculating statistics in database

Options:
  --help  Show this message and exit.

Commands:
  clean     Clean 'stats' key in all files
  generate  Group of time-consuming function.
```

