import dbauth
import pyodbc


class MssqlDatabase(object):

    def odbc_connection(self, service_type):
        login = dbauth.databases[service_type]["login"]
        password = dbauth.databases[service_type]["password"]
        server = dbauth.databases[service_type]["server"]
        database = dbauth.databases[service_type]["database"]
        return pyodbc.connect('DRIVER=FreeTDS;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s' % (server, database, login, password))

    def build_select_query(self, columns, table, where):
        where_prepend = ""
        if len(where) > 0:
            where_prepend = "AND"
        columnstr = ", ".join(columns)
        return "SELECT %s FROM %s WHERE 1=1 %s %s" % (columnstr, table, where_prepend, where)

    def select_all(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
