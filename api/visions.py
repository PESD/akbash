"""
Visions Module

Goals:
* Setup a database connection
* Basic functions to query the database
* Classes based on database views

We're not using django models because django does a lot of automatic things
when you configure a database in in the settings files. We don't want those
automatic things to happen with 3rd party databases.

Using a read only account to connect. This module is assuming read-only access.
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
       [fieldname[0] for fieldname in cursor.description] # list of field names
    """
    return [row for row in cursor.fetchall()]


"""
Some classes to make it easier to grab data from the Visions DB.
"""

class Select():

    def __init__(self, columns=None, table=None, where_str=None, **kwargs):

        # By default the class doesn't make use of paramaterized queries but
        # they can be very useful so let's put some support in.
        # Params should be a string containing each param separated by commas.
        # should I make a set_params method? I should add params to the
        # arguments the class accepts when initialized.
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
        # TODO: should I raise an error if where_str and kwargs are both
        # present? Or should I allow both and just join them together?
        self.where_str = where_str
        # In kwargs, wrap str values in single quotes
        if kwargs:
            for i in kwargs:
                if isinstance(kwargs[i], str):
                    kwargs[i] = "'" + kwargs[i] + "'"
            # pop one item off to start out self.where_str
            x = kwargs.popitem()
            self.where_str = x[0] + " = " + str(x[1])
            if kwargs:
                for kw in kwargs:
                    self.where_str += " and " + kw + " = " + str(kwargs[kw])

        self.sql = self.build_sql()


    def build_sql(self):
        "Assemble a string containing an SQL statement."
        stmt = "select " + self.columns
        if self.table:
            stmt += " from " + self.table
        if self.where_str:
            stmt += " where " + self.where_str
        # Null out some invalid queries
        if stmt == 'select *':
            stmt = None
        if self.table is None and self.where_str is not None:
            stmt = None
        if self.columns is None:
            stmt = None
        return stmt


    # A general purpose method to execute the sql statement.
    def execute(self):
        """Execute the sql statement and return a cursor.

        Execute the statment in self.sql using self.params if it's set.
        """
        if self.params:
            self.cursor = exec_sql(self.sql, self.params)
        else:
            self.cursor = exec_sql(self.sql)
        return self.cursor
    # an alias to execute()
    fetch_cursor = execute


    # Execute the sql statement and return row or dict objects.
    #
    # These loads all rows into memory. Instead, iterate through the cursor if
    # you know the query will return a huge amount of data.
    def fetch_all_row(self):
        """Execute the sql statement and return all rows as a list of row
        objects.
        """
        cursor = self.execute()
        return rowfetchall(cursor)

    def fetch_all_dict(self):
        """Execute the sql statement and return all rows as a list of
        dictionary objects.
        """
        cursor = self.execute()
        return dictfetchall(cursor)


    # what the doc string says
    def fetch_value(self):
        """Execute the sql statement and return the value in the first column
        of the first row"""
        cursor = self.execute()
        result = cursor.fetchone()
        return result[0]


    """
    Generate methods named after each column in the table where you
    give the visions ID and the value in that column is returned. The class
    variable "table" must be defined.

    Luckily there are no spaces in table names in the visions DB. I don't know
    how this code would handle table names with spaces. I didn't test that.
    """

    # Only provide 1 column name. Only query ID primary key so only 1 row is
    # returned. This breaks otherwise.
    # TODO: Do I need to check for multiple rows and raise an error if so?
    @staticmethod
    def get_column_by_id(column, table, idnum):
        "Retrive a column value filtered by the ID primary key column."
        cursor = exec_sql(
            "select " + column + " from " + table + " where ID = " + str(idnum))
        results = cursor.fetchone()
        if results is not None:
            return results[0]


    # There is a chance an attribute name clashes with a db column name.
    # Consider adding a prefix to the generated method name. Like get_name.
    # No conflics that I see with the tables we're using presently.
    @classmethod
    def make_column_by_id_methods(cls):
        if not cls.table:
            return None  # should I raise an error instead?

        # get a list of column names
        # I could have used cursor.columns(table='cls.table'). Is that better?
        sql = "select top 1 * from " + cls.table
        cursor = exec_sql(sql)
        columns = []
        for r in cursor.description:
            columns.append(r[0])

        # Iterate through column names and make a method for each column
        for c in columns:
            def get_by_id(cls, idnum, column=c, table=cls.table):
                return cls.get_column_by_id(column, table, idnum)
            setattr(cls, c, classmethod(get_by_id))




class Viwpremployees(Select):
    "Contains methods to query the viwPREmployees view in Visions."

    table = "viwPREmployees"

    def __init__(self, columns=None, where_str=None, **kwargs):
        super().__init__(columns, self.table, where_str, **kwargs)
        self.make_column_by_id_methods()


class Viwprpositions(Select):
    "Contains methods to query the viwPRPositions view in Visions."

    table = "viwPRPositions"

    def __init__(self, columns=None, where_str=None, **kwargs):
        super().__init__(columns, self.table, where_str, **kwargs)
        self.make_column_by_id_methods()
