# The api.visions Module
**An interface to query data from the Visions database.**
There are many ways you can retreive visions data through this module. You can run straight SQL queries or you can use various class methods that try to make things easier for you.
## Configuration
In the configurations .ini file:
```ini
[visions database]
NAME: dbname
USER: username
PASSWORD: password
OPTIONS-DSN: VSDB
```
## Raw Database Queries
### exec_sql(sql, *params, timeout=None)
* **sql**: a string containing an sql statement
* **params**: [Dynamic SQL parameters](https://github.com/mkleehammer/pyodbc/wiki/Getting-started#parameters)
* **timeout**: A timeout for the connection, in seconds. None for no timeout. If you get *OperationalError* errors it could be because the timeout was reached.

This function will create the database connection then execute the SQL statement. The results are returned in a cursor. See the [pyodb documentation](https://github.com/mkleehammer/pyodbc/wiki/Getting-started#selecting-some-data) for more information on working with cursors and the row objects contained in the cursor.
## The Select Class

