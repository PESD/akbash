"""
Visions

Database connection and model
"""

import os
import pyodbc
from configparser import ConfigParser
from django.conf import settings

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
vsdbcscript = (
    'DSN=' + config['visions database']['OPTIONS-DSN'] +
    ';PWD=' + config['visions database']['PASSWORD'] +
    ';DATABASE=' + config['visions database']['NAME'] +
    ';UID=' + config['visions database']['USER']
)

# Establish visions DB connection
# using the with statement in pyodb doesn't close the connection?
# Changing to use try: finally:.
# https://github.com/mkleehammer/pyodbc/wiki/Connection#connection-objects-and-the-python-context-manager-syntax
try:
    vsdbconn = pyodbc.connect(vsdbcscript, autocommit=False)

    # doc says to set the encoding. I'm not sure I have this right.
    vsdbconn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    vsdbconn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    vsdbconn.setencoding(encoding='utf-8')

    # Set queries on the connection to timeout. eg., 60 seconds.
    # If OperationalError is raised, it might be a query timeout.
    # vsdbconn.timeout = 60

    # Create a cursor
    with vsdbconn.cursor() as cursor:

        # run a query
        cursor.execute("select @@VERSION")
        row = cursor.fetchone()
        if row:
            print(row)
finally:
    vsdbconn.close()
