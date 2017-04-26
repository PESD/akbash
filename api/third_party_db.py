"""
Setup 3rd party databases.

Django does a lot of automatic things when you configure a database in in the
settings files. We don't want those automatic things to happen with 3rd party
databases.
"""

import os
import pyodbc
from configparser import ConfigParser
from django.conf import settings

# load in private seettings from the ini file
private_config_file = os.environ.get(
    'AKBASH_CONFIG_FILE',
    os.path.join(settings.BASE_DIR, '..', 'akbash_private_settings', 'akbash.ini'))
config = ConfigParser(interpolation=None)
config.read(private_config_file)

# check visions database config for unrecognized options.
for k in config['visions database']:
    if k.startswith('option'):
        continue
    elif k.startswith('test'):
        continue
    elif k.upper() in (
            'ATOMIC_REQUESTS',
            'AUTOCOMMIT',
            'ENGINE',
            'HOST',
            'NAME',
            'CONN_MAX_AGE',
            'PASSWORD',
            'PORT',
            'TIME_ZONE',
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
with pyodbc.connect(vsdbcscript) as vsdbconn:

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
