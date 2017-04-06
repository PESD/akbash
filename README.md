# akbash

[![Build Status](http://circleci-badges-max.herokuapp.com/img/PESD/akbash?token=505e27dc7bacf1bdc368d12374285a8255509700)](https://circleci.com/gh/PESD/akbash)

## Installation

1. Set up a Virtualenv
2. `pip install -r requirements.txt`
3. Create configuration file (see below)
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. To manually populate the database: `python cron.py`
6. Add cron.py to crontab to automatically update django

## Apps

### api

The `api` app will hold ETL and data model things.

### bpm

The `bpm` app will handle business logic, workflow, etc.

### etl

The `etl` app (not created yet) will hold ETL functionality.

## Starting from Scratch

To wipe out your database and start from scratch without having to worry about migrations:

1. Delete or drop database
2. Delete all migration files from each app's ./migration directory (make sure not to delete \_\_init\_\_.py in those directories)

## Configuration File
Local settings and sensitive information are stored in an .ini syle configuration file. By default the file, akbash.ini, is located besides the base directory in a directory named akbash_private_settings (```BASE_DIR\..\akbash_private_settings\akbash.ini```). You may set "AKBASH_CONFIG_FILE" as an environment variable with your own filename and location. Refer to the example below and settings.py for what you should put in the config file.

```
[secrets]
SECRET_KEY: 
TALENTED_API_KEY: 

[default database]
DATABASE_ENGINE: django.db.backends.sqlite3
DATABASE_NAME: db.sqlite3
DATABASE_USER: 
DATABASE_PASSWORD: 
DATABASE_DRIVER: 
DATABASE_DSN: 

[debug]
DEBUG: True
```

### TalentEd API Key

For the xml_request script to work, enter the api key in the configuration file.

## Connecting to SQL Server
### FreeTDS
Install FreeTDS. Add the following to freetds.conf.
```
[VSQL]
  host = ms-27-vsql-1
  port = 1433
```

### unixodbc
Install unixodbc. Add the following to odbc.ini.
```
[VSQL]
Description         = Versifit SQL Server
Driver              = FreeTDS
Servername          = VSQL
```

### akbash.ini
```
[default database]
DATABASE_ENGINE: sql_server.pyodbc
DATABASE_NAME: akbash
DATABASE_USER: akbash
DATABASE_PASSWORD: password
DATABASE_DRIVER: FreeTDS
DATABASE_DSN: VSQL
```
