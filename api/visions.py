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
#   Multiple cursors inside transaction make sense. I'm not sure how this
#   decision will effect paramaterized queries. I think SQL server will cache
#   the query plan so it will be okay maybe?
#   I'm starting to question this decision.
def exec_sql(sql, *params, timeout=None):
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
    if params:
        results = cursor.execute(sql, params)
    else:
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

I'm not yet clear in my brain wether to use classes or functions
"""

class Select():

    def __init__(self, columns=None, table=None, where_str=None, **kwargs):

        # By default the class doesn't make use of paramaterized queries but
        # they can be very useful so let's put some support in.
        # should I make a set_params method?
        self.params = None

        # The Select clause in a sql statement
        if isinstance(columns, str):
            self.columns = columns
        elif isinstance(columns, (list, tuple)):
            self.columns = ", ".join(columns)
        else:
            self.columns = "*"

        # The From clause in a sql statement
        self.table = table

        # The Where clause in a sql statement
        #   Notice that you can't provide both where_str and kwargs when
        #   calling the class.
        self.where_str = where_str
        if kwargs:
            x = kwargs.popitem()
            self.where_str = x[0] + " = " + str(x[1])
            if kwargs:
                for kw in kwargs:
                    self.where_str += ", " + kw + " = " + str(kwargs[kw])

        self.sql = self.build_sql()


    def build_sql(self):
        "Assemble a string containing an SQL statement."
        stmt = "select " + self.columns
        if self.table:
            stmt += " from " + self.table
        if self.where_str:
            stmt += " where " + self.where_str
        if stmt == 'select *':
            stmt = None
        return stmt


    def where_id(self, table: str, idnum: int):
        "Query by ID. A cursor is returned."
        self.cursor = exec_sql(
            "select * from ? where ID = ?", table, idnum)
        return self.cursor


    # A general purpose method to execute the sql statement.
    # Execute the statment in self.sql using self.params if it's set.
    def execute(self):
        if self.params:
            self.cursor = exec_sql(self.sql, self.params)
        else:
            self.cursor = exec_sql(self.sql)
        # will this copy the cursor? I need to experiment.
        x = self.cursor
        return rowfetchall(x)

    # I'm not sure what I'm doing here. do I return the cursor even though it's
    # in self.cursor? I could return the results in a list of row objects. This
    # is the general execute method so I think I should go with the list of
    # rows and use other methods to return more specific things.


class Viwpremployees(Select):
    "Contains methods to query the viwPREmployees view in Visions."

    table = "viwPREmployees"


class Viwprpositions(Select):
    "Contains methods to query the viwPRPositions view in Visions."
    table = "viwPRPositions"
