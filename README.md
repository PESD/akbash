# akbash

[![Build Status](http://circleci-badges-max.herokuapp.com/img/PESD/akbash?token=505e27dc7bacf1bdc368d12374285a8255509700)](https://circleci.com/gh/PESD/akbash)

## Installation

1. Set up a Virtualenv
2. `pip install -r requirements.txt`
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

## TalentEd API Key

For the xml_request script to work, an `api_keys.py` file needs to exist in the `bpm` app directory. Check out the sample in there for how it should look. Or see here:

```keys = {
    "talented": {
        "sKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }
}```
