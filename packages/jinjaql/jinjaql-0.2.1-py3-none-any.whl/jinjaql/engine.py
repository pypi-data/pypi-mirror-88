import sqlite3
import os

def default(query_string: str, connection_string: str):
    """
    For the default behavior, the engine returns the query string
    :param query_string: This is the raw query string that the SQL engine would use to return the data
    :param connection: This is the connection string that comes from the SQL template that can be used for the SQL query
    :return: The default will return the string w/o changes to keep the default SNAQL behavior, but any additional
    would return data (ie DataFrame)
    """
    return query_string

def sqlite_test(query_string: str, connection_string: str):
    """
    This is a simple sqlite engine for integration testing
    :param query_string: This is the raw query string that the SQL engine would use to return the data
    :param connection: This is the connection string that comes from the SQL template that can be used for the SQL query
    :return:
    """

    sql_root = os.path.abspath(os.path.dirname(__file__))
    sqlite_folder = os.path.join(sql_root, 'tests', 'data')
    sqlite_path = os.path.join(sqlite_folder, connection_string)
    connection = sqlite3.connect(sqlite_path)

    try:
        result = connection.execute(query_string)
        output = result.fetchall()
        connection.commit()
    except Exception as e:
        output = e
    finally:
        connection.close()


    return output