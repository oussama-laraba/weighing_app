from models.database_connection import database_connection

class ServerModel():

    def __init__(self):
        self.db = database_connection()

    def select_query(self, columns='*', conditions= None):
        print("perform query select")
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM SERVER'
        
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0].upper()+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'

        print(query)
        data = cursor.execute(query).fetchall()
        cursor.close()
        return data
        

    def create_query(self, data):
        cursor = self.db.cursor()
        
        id = cursor.execute('INSERT INTO SERVER\
                    (URL, PORT, DATABASE, KEY)\
                    VALUES ("{}", {}, "{}", "{}");'.format(
                        data.get('URL'),
                        data.get('PORT'),
                        data.get('DATABASE'),
                        data.get('KEY')
                    )).lastrowid
        cursor.close()
        self.db.commit()
        return id

    def update_query(self, data):
        cursor = self.db.cursor()

        cursor.execute('UPDATE SERVER SET\
                        URL = "{}" , PORT = {}, DATABASE = "{}", KEY = "{}"\
                        WHERE ID = {};'.format(
                            data.get('URL'),
                            data.get('PORT'),
                            data.get('DATABASE'),
                            data.get('KEY'),
                            data.get('ID')
                        ))
        cursor.close()
        self.db.commit()
        print('update query')

    def delete_query(self, id):
        cursor = self.db.cursor()
        cursor.execute(f'DELETE FROM SERVER WHERE ID = {id};')
        cursor.close()
        self.db.commit()
        print('perform delete')

    