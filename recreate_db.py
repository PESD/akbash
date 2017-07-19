"""
Drop all tables in the default database and remove migration files.
This is a MS SQL Server specific. This won't work with sqlite.

The SQL code was grabbed from here:
http://stackoverflow.com/questions/8439650/how-to-drop-all-tables-in-a-sql-server-database

I didn't know about management commands like, syncdata, reset_db, and flush,
when I created this script. They don't work with MS SQL Server so this script
is still useful.
"""

import os
import sys
from django.conf import settings
from django.db import connection
from subprocess import run
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")

# For asking y/n questions
def prompt(query):
    sys.stdout.write('%s [y/n]: ' % query)
    val = input()
    if val.lower() in ('y', 'yes'):
        return True
    elif val.lower() in ('n', 'no'):
        return False
    else:
        sys.stdout.write('Please answer with a y/n\n')
        return prompt(query)


# Transact-SQL scripts
# Foreign key constraints must 1st be dropped before tables can be dropped
tsql1 = """\
DECLARE @Sql NVARCHAR(500) DECLARE @Cursor CURSOR

SET @Cursor = CURSOR FAST_FORWARD FOR
SELECT DISTINCT sql = 'ALTER TABLE [' + tc2.TABLE_NAME + '] DROP [' + rc1.CONSTRAINT_NAME + ']'
FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc1
LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc2 ON tc2.CONSTRAINT_NAME =rc1.CONSTRAINT_NAME

OPEN @Cursor FETCH NEXT FROM @Cursor INTO @Sql

WHILE (@@FETCH_STATUS = 0)
BEGIN
Exec sp_executesql @Sql
FETCH NEXT FROM @Cursor INTO @Sql
END

CLOSE @Cursor DEALLOCATE @Cursor
"""

# Drop all tables script
tsql2 = "EXEC sp_MSforeachtable 'DROP TABLE ?'"

# Drop tables
db = settings.DATABASES['default']['NAME']
engine = settings.DATABASES['default']['ENGINE']
if prompt("Delete all tables from the default database, {}?".format(db)):
    with connection.cursor() as cursor:
        if engine == 'sql_server.pyodbc':
            cursor.execute(tsql1)
            cursor.execute(tsql2)
        else:
            print(
                "This script only support MS SQL Server databases.\n"
                "Database Engine: {}".format(engine))

# Delete migration files
BASE_DIR = settings.BASE_DIR
cmd1 = 'find {} -path "*/migrations/*.py" -not -name "__init__.py" -delete -print'.format(BASE_DIR)
cmd2 = 'find {} -path "*/migrations/*.pyc"  -delete -print'.format(BASE_DIR)

if prompt("\nDelete migration files?"):
    run(cmd1, shell=True)
    run(cmd2, shell=True)

# rerun migrations
if prompt("\nMake migrations and migrate?"):
    execute_from_command_line(['', 'makemigrations'])
    execute_from_command_line(['', 'migrate'])

# Load fixtures
fixtures = [
    "akjob_dayofweek.json",
    "akjob_dayofmonth.json",
]

print("\nFixtures: " + str(fixtures))
if prompt("Load fixtures?"):
    execute_from_command_line(['', 'loaddata'] + fixtures)
