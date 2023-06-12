import sqlite3
import os
import psutil


class DbConnection():
    def __init__(self, *args, **kwargs):
        self.db = self.database_connection()


    def database_connection(self):
        try:
            sqliteConnection = sqlite3.connect('weighing.db')
            cursor = sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")

            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            return sqliteConnection

        except sqlite3.Error as   error:
            print("Error while connecting to sqlite", error)


