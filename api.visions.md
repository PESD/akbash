# The api.visions Module
**An interface to query data from the Visions database.**
There are many ways you can retreive visions data through this module. You can run straight SQL queries or you can use various class methods that try to make things easier for you.
## Configuration
In your ODBC configuration, add a DSN for the visions database. In the akbash configurations .ini file:
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

***example:***
```python
>>> result = exec_sql("select Name from viwPREmployees where ID = ?", 7965)
>>> result
<pyodbc.Cursor object at 0x105a45150>
>>> result.fetchone()
('STONE, RAY ', )
```
### Functions to help retreive data from the cursor
These functions retreive all rows from a cursor. It's recommend to use the ```rowfetchall``` function over ```dictfetchall```. When using these functions, be mindful you will be loading all results into memory. For this reason, it's best to iterate through the cursor for queries that return results larger then what you want in memory.
#### dictfetchall(cursor)
Returns all rows from a cursor as a list of dictionaries.
```python
>>> result = api.visions.exec_sql("select top 2 ID, LastName, FirstName from viwPREmployees")
>>> emp = api.visions.dictfetchall(result)
>>> emp
[{'ID': 7965, 'LastName': 'STONE', 'FirstName': 'RAY'}, {'ID': 5465, 'LastName': 'CLAYTON', 'FirstName': 'BARBARA'}]
>>> [r['LastName'] for r in emp]
['STONE', 'CLAYTON']
```
#### rowfetchall(cursor)
Return all rows from a cursor as a list of row objects. Row object behave similarly to a list of tuples. You can get column values by index or column name.
```python
>>> result = api.visions.exec_sql("select top 2 ID, LastName, FirstName from viwPREmployees")
>>> emp = api.visions.rowfetchall(result)
>>> emp
[(7965, 'STONE', 'RAY'), (5465, 'CLAYTON', 'BARBARA')]
>>> emp[0][0] # first column in the first row.
7965
>>> emp[0].ID # ID column in the first row
7965
>>> [fieldname[0] for fieldname in result.description] # list of field names
['ID', 'LastName', 'FirstName']
```
## The Select Class

