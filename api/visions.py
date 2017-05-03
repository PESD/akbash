"""
Visions

Database connection and model
"""

import os
import pyodbc
from configparser import ConfigParser
from django.conf import settings
from django.db import models
# from collections import namedtuple


"""
Setup visions database.
Django does a lot of automatic things when you configure a database in in the
settings files. We don't want those automatic things to happen with 3rd party
databases.
"""

# load in private seettings from the ini file
private_config_file = os.environ.get(
    'AKBASH_CONFIG_FILE',
    os.path.join(settings.BASE_DIR, '..', 'akbash_private_settings', 'akbash.ini'))
config = ConfigParser(interpolation=None)
config.read(private_config_file)

# check visions database config for unrecognized options.
for k in config['visions database']:
    if k.upper() in (
            'OPTIONS-DSN',
            'NAME',
            'PASSWORD',
            'USER'):
        continue
    else:
        raise KeyError("Unrecognized visions database option: {}".format(k))

# Visions DB connecrtion string
cstring = (
    'DSN=' + config['visions database']['OPTIONS-DSN'] +
    ';PWD=' + config['visions database']['PASSWORD'] +
    ';DATABASE=' + config['visions database']['NAME'] +
    ';UID=' + config['visions database']['USER']
)

# Establish visions DB connection
# reading the docs, it's probably best not use use multiple cursors in
# a connection since cursors are not isolated. Will keep to one cursor per connection.
# The exception would be doing things inside transactions. Multiple cursors in
# the transaction might make sense.
def exec_sql(sql, timeout=None):
    """Execute SQL statement and return the results as a cursor object."""
    connection = pyodbc.connect(cstring, autocommit=False)

    # doc says to set the encoding. I'm not sure I have this right.
    connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    connection.setencoding(encoding='utf-8')

    # Set queries on the connection to timeout. eg., 60 seconds.
    # If OperationalError is raised, it might be a query timeout.
    # TODO: re-read the connection.timeout info. relookup function defaults and
    #   optional function paramaters.
    if timeout:
        connection.timeout = timeout

    # Create a cursor
    cursor = connection.cursor()

    # execute the sql and return results as a cursor object
    results = cursor.execute(sql)
    return results

# From https://docs.djangoproject.com/en/1.11/topics/db/sql under
# Performing Raw Queries
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# iterate through retreived rows and load them into a model?  or create a
# object factory to supply only the needed data.  an object factory sounds more
# sensable so whole tables are not loaded into memory.


# Classes for Visions tables and views
class VsPREmployees():
    pass


# Model - I'm starting to think using django model objects isn't the way to go.
class VsModel(models.Model):
    class Meta:
        abstract = True
        managed = False

class VsPerson(VsModel):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    badge_number = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    race_white = models.BooleanField(default=False)
    race_asian = models.BooleanField(default=False)
    race_black = models.BooleanField(default=False)
    race_islander = models.BooleanField(default=False)
    race_american_indian = models.BooleanField(default=False)
    ethnicity = models.CharField(max_length=50)
    hqt = models.CharField(max_length=16)
    ssn = models.CharField(max_length=9)

    class Meta:
        abstract = True
