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
## Table and view classes
Currently there are two classes, **Viwpremployees** and **Viwprpositions**. These are subclasses of the Select class which are set to use a specific table or view in the Visions database. In addition methods available in the Select class, there are methods for each column in the table of view. Calling the column method with and ID number turns the value in that column associated with the given ID number.
```python
>>> import api.visions
>>> name = api.visions.Viwpremployees().Name(5416)
>>> name
'YOUKHANNA, PAOLA  '
```
## The Select Class
You can use the Select class to query data from Visions tables.
### select(columns=None, table=None, where_str=None, **kwargs)
* **columns**: The columns you want to select. This should be a string with the columns names separated by commas, like in a SQL query. You can also use a list or tuple containing the column names.
* **table**: A string containing the table name to be queried.
* **where_str**: This is a string containing the Where clause of a SQL Select statement. If kwargs are given, they will overwrite where_str.
* **kwargs**: Key value pairs that are used in the Where clause of a SQL Select statement. ```key1 = 'value1', key2 = 'value2'``` will appear as ```key1='value1', key2='value2'``` in the Where clause of the generated SQL statement.

The Select class will build an SQL query from the variables provided above and assign it to ```Select.sql```. The ```Select.build_sql``` method builds the query and returns the SQL statement.
### Select.params
 You can use dynamic SQL by assigning the ```params``` variable. See the [pyodbc documentation](https://github.com/mkleehammer/pyodbc/wiki/Getting-started#parameters) for more information.
### Select.execute()
To execute the query and return the pyodbc cursor. The cursor is also assigned to ```Select.cursor```.
### Select.fetch_value()
Execute the SQL statement in ```Select.sql``` and return the value in the first column in the first row.
```python
>>> vsquery = api.visions.Select("Name", "viwPREmployees", ID = 6527)
>>> vsquery.fetch_value()
'YOUKHANNA, PAOLA  '
```
### Select.fetch_all_row() and Select.fetch_all_dict()
Returns all rows in the cursor as row objects or dictionaries.
### Examples
```python
>>> vsquery = api.visions.Select("ID, Name", "viwPREmployees", ID = 6527)
>>> vsquery.sql
'select ID, Name from viwPREmployees where ID = 6527'
>>> result = vsquery.execute()
>>> result
<pyodbc.Cursor object at 0x10a3be0f0>
>>> id_name = vsquery.fetch_all_row()
>>> id_name
[(6527, 'YOUKHANNA, PAOLA  ')]
>>> result = api.visions.Select("Name", "viwPREmployees", ID = 6527).execute()
>>> result.fetchone().Name
'YOUKHANNA, PAOLA  '
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
