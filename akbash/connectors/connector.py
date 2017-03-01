from abc import ABCMeta, abstractmethod
import db


# Abstract Factory Connector
class Connector(object):

    @staticmethod
    def type(connector_type):
        if connector_type == "visions":
            return VisionsConnector()
        raise TypeError('Unknown Connector Type')


# Abstract Interface Connection
class Connection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_result(columns, table, where):
        pass


# Each connector needs a concrete connector factory (ZzzConnector) /
# and a concrete interface (ZzzConnection)

class VisionsConnector(object):
    def get_connection(self):
        return VisionsConnection()


class VisionsConnection(Connection):
    def select_result(self, columns, table, where):
        visions_db = db.MssqlDatabase()
        visions_connection = visions_db.odbc_connection("visions")
        query = visions_db.build_select_query(columns, table, where)
        return visions_db.select_all(query, visions_connection)


# Temp test for command-line test for command lines. Should be /
# turned into an actual test.

if __name__ == "__main__":
    connector = Connector.type("visions")
    connection = connector.get_connection()
    columns = [
        "Name",
        "DAC",
        "EmployeeID"
    ]
    a = connection.select_result(columns, "viwPRPositions", "PositionType = 'Open'")
    for b in a:
        if len(b.Name) > 0:
            print(b.Name)
