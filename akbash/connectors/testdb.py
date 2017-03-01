import pyodbc
import dbauth

# Vars assigned in dbauth.py which is ignored in the repo. Get this file from Troy.
login = dbauth.databases["visions"]["login"]
password = dbauth.databases["visions"]["password"]
server = dbauth.databases["visions"]["server"]
database = dbauth.databases["visions"]["database"]

connection = pyodbc.connect('DRIVER=FreeTDS;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s' % (server, database, login, password))

try:
    cursor = connection.cursor()
except e:
    if e.__class__ == pyodbc.ProgrammingError:
        print("DB Error")

print("DB Okay")
