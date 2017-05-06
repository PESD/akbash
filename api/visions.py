"""
Visions

* Setup a database connection
* Basic functions to query the database
* Classes based on database views

We're not using django models because django does a lot of automatic things
when you configure a database in in the settings files. We don't want those
automatic things to happen with 3rd party databases.
"""


import os
import pyodbc
from configparser import ConfigParser
from django.conf import settings


"""
Visions database connection
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

# Establish visions DB connection and execute statements
#   Reading the docs, it's probably best not use use multiple cursors in a
#   connection since cursors are not isolated. Will keep to one cursor per
#   connection. The exception would be doing things inside transactions.
#   Multiple cursors inside transaction make sense.
def exec_sql(sql, timeout=None):
    "Execute SQL statement and return the results as a cursor object."
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


"""
Functions to help retreive data from the cursor
"""

# From https://docs.djangoproject.com/en/1.11/topics/db/sql under
# Performing Raw Queries
def dictfetchall(cursor):
    "Return all rows from a cursor as a list of dictionaries."
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# it might be faster to just use the row objects returned by the cursor?
def rowfetchall(cursor):
    """Return all rows from a cursor as a list of row objects.

    You can get column values by index or column name.

    Examples:
       result[0][0] # first column in the first row.
       result[0].ID # ID column in the first row
       fieldname[0] for fieldname in cursor.description] # list of field names
    """
    return [row for row in cursor.fetchall()]


"""
Some classes to make it easier to grab data from the Visions DB.

For referance, viwpremployees and viwprpositions as models
https://github.com/PESD/akbash/blob/0ce23430567945443bb465ba0003a84a1336af1f/api/visions_models.py
"""

class Select():

    def __init__(self, columns=None, table=None, where_str=None, **kwargs):

        # For the From clause in a sql statement
        if table:
            self.table = table

        # For the Select clause in a sql statement
        if isinstance(columns, str):
            self.columns = columns
        elif isinstance(columns, (list, tuple)):
            self.columns = ", ".join(columns)
        else:
            self.columns = "*"

        # For the Where clause in a sql statement
        if where_str:
            self.where_str = where_str
        elif kwargs:
            self.x = kwargs.popitem()
            self.where_str = self.x[0] + " = " + str(self.x[1])
            if kwargs:
                for kw in kwargs:
                    self.where_str += ", " + kw + " = " + str(kwargs[kw])


    def where_id(self, id):
        "Query by ID. A cursor is returned."
        # TODO: fix this
        cursor = exec_sql(
            "select * from viwPREmployees where ID = ?",)
        return cursor


    def where(self, **kwargs):
        pass


class Viwpremployees(Select):
    "Contains methods to query the viwPREmployees view in Visions."
    table = "viwPREmployees"


class Viwprpositions(Select):
    "Contains methods to query the viwPRPositions view in Visions."
    table = "viwPRPositions"
