# akbash

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

## Starting from Scratch

To wipe out your database and start from scratch without having to worry about migrations:

1. Delete or drop database
2. Delete all migration files from each app's ./migration directory (make sure not to delete \_\_init\_\_.py in those directories)
