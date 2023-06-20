
class ServerModel():
    def __init__(self, db=None):
        self.db = db


    def select_query(self, columns='*', conditions= None):
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM server'
        print(conditions)
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0]+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'
        print(query , '\n')

        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records


    def create_query(self, data):
        cursor = self.db.cursor()
        
        cursor.execute('INSERT INTO server\
                    (URL, PORT, DATABASE_NAME)\
                    VALUES ("{}", {}, "{}");'.format(
                        data.get('url'),
                        data.get('port'),
                        data.get('database'),
                    ))
        id = cursor.lastrowid
        print(id)
        cursor.close()
        self.db.commit()
        return id


    def update_query(self, data):
        cursor = self.db.cursor()
        cursor.execute('UPDATE SERVER SET\
                        URL = "{}" , PORT = {}, DATABASE_NAME = "{}"\
                        WHERE id = {};'.format(
                            data.get('url'),
                            data.get('port'),
                            data.get('database'),
                            data.get('id')
                        ))
        cursor.close()
        self.db.commit()


    def delete_query(self, id):
        cursor = self.db.cursor()
        cursor.execute(f'DELETE FROM SERVER WHERE ID = {id};')
        cursor.close()
        self.db.commit()