import sqlite3
import mysql.connector
from mysql.connector import errorcode

class DbConnection():
    def __init__(self, *args, **kwargs):
        self.db = self.mysql_database_connection()
        # self.db = self.database_connection()


    def database_connection(self):
        try:
            sqliteConnection = sqlite3.connect('weighing.db')
            print("Database created and Successfully Connected to SQLite")
            return sqliteConnection

        except sqlite3.Error as   error:
            print("Error while connecting to sqlite", error)

    def mysql_database_connection(self):
        config = {
                'user': 'root',
                'password': '123456',
                'host': 'localhost',
                'database': 'weighing',
                'raise_on_warnings': True
                }
        try:
            mysqlConnection = mysql.connector.connect(**config)
            print("Database created and Successfully Connected to MySQL")
            return mysqlConnection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

