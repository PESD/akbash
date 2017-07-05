# akbash

[![Build Status](http://circleci-badges-max.herokuapp.com/img/PESD/akbash?token=505e27dc7bacf1bdc368d12374285a8255509700)](https://circleci.com/gh/PESD/akbash)

## Installation

1. Install unixodbc package
2. Install freetds package (see [MSSQL Setup](#mssql-setup))
3. Set up a Virtualenv
4. `pip install -r requirements.txt`
5. Create configuration file (see below)
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8. To manually populate the database: `python cron.py`
9. Add cron.py to crontab to automatically update django

## Ubuntu packages

We are using Ubuntu here at PESD. Here are the packages we are using:

* `apache2`
* `apache2-dev`
* `libapache2-mod-wsgi-py3`
* `unixodbc`
* `unixodbc-dev`
* `unixodbc-bin`
* `tdsodbc`
* `freetds-bin`
* `freetds-common`
* `freetds-dev`
* `python3`
* `python3-dev`
* `python3-pip`


## MSSQL Setup

unixodbc and freetds need to be installed on the server. For Ubuntu, run the following commands, install the following packages via apt: `unixodbc unixodbc-dev unixodbc-bin tdsodbc freetds-bin freetds-common freetds-dev`

You must edit `/etc/freetds/freetds.conf` and add all SQL servers you need to connect to. Here is an example:

```
[VSQL]
        host = your.sqlserver.hostname
        port = 1433
        tds version = 8.0

[VSDB]
        host = your.visions.hostname
        port = 1433
        tds version = 8.0
```

*Note: It is important to use tds version 8.0*

You must also edit `/etc/odbcinit.ini` to specify where to find the tdsodbc drivers:

```
[FreeTDS]
Description = TD Driver (MSSQL)
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
FileUsage = 1
```

Finally, you must edit `/etc/odbc.ini`. Here is an example:

```
[VSQL]
Description         = My SQL Server
Driver              = FreeTDS
Servername          = VSQL
TDS_Version         = 8.0

[VSDB]
Description         = Visions SQL Server
Driver              = FreeTDS
Servername          = VSDB
TDS_Version         = 8.0
```

To configure Akbash to use your SQL server, see [Configuration File](#configuration-file)

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

## JSON Web Token Authentication

Akbash uses JSON Web Tokens (JWT) for authentication. This can be turned on and off in the [Configuration File](#configuration-file). When on, the browser or application MUST send a valid token to retrieve any information.

## Configuration File
Local settings and sensitive information are stored in an .ini style configuration file. By default the file, akbash.ini, is located besides the base directory in a directory named akbash_private_settings (```BASE_DIR\..\akbash_private_settings\akbash.ini```). You may set "AKBASH_CONFIG_FILE" as an environment variable with your own filename and location. Refer to the example below and settings.py for what you should put in the config file.

```
[secrets]
SECRET_KEY:
TALENTED_API_KEY:

[default database]
ENGINE: django.db.backends.sqlite3
NAME: db.sqlite3
USER:
PASSWORD:
OPTIONS-DRIVER:
OPTIONS-DSN:

[visions database]
NAME: dbname
USER: username
PASSWORD: password
OPTIONS-DSN: VSDB

[debug]
DEBUG: True

[security]
ALLOWED_HOSTS: 127.0.0.1, localhost
ENABLE_JWT: False

[email]
EMAIL_HOST: outlook.office365.com
EMAIL_PORT: 587
EMAIL_HOST_USER: youremail@yourdomain.com
EMAIL_HOST_PASSWORD: yourpassword
EMAIL_USE_TLS: True

[ldap]
LDAP_SERVER: ad_server.example.com
LDAP_DOMAIN: example.com
LDAP_USER: username
LDAP_PASSWORD: password
LDAP_SEARCH_BASE: dc=example,dc=com
```

### TalentEd API Key

For the xml_request script to work, enter the api key in the configuration file.
