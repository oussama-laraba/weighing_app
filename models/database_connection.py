import sqlite3


class DbConnection():
    def __init__(self, *args, **kwargs):
        self.db = self.database_connection()


    def database_connection(self):
        try:
            sqliteConnection = sqlite3.connect('weighing.db')
            print("Database created and Successfully Connected to SQLite")
            return sqliteConnection

        except sqlite3.Error as   error:
            print("Error while connecting to sqlite", error)


