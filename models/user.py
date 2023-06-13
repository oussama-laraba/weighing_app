


class UserModel():

    def __init__(self, db=None):
        self.db = db

    def get_data(self):
        cursor = self.db.cursor()
        users = cursor.execute('SELECT U.ID, U.EMAIL, U.PASSWORD, S.URL, U.COMPANY\
                        FROM USER as U\
                        INNER JOIN  SERVER as S ON U.URL_ID = S.ID').fetchall()
        cursor.close()
        return users
        
    
    def select_query(self, columns='*', conditions= None):
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM USER'
        
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
        id = cursor.execute('INSERT INTO USER \
                    (EMAIL, PASSWORD, URL_ID, COMPANY)\
                    VALUES ("{}", "{}", "{}", "{}");'.format(
                        data.get('EMAIL'),
                        data.get('PASSWORD'),
                        data.get('URL_ID'),
                        data.get('COMPANY')
                    )).lastrowid
        cursor.close()
        self.db.commit()
        return id

    def update_query(self, data):
        cursor = self.db.cursor()

        cursor.execute('UPDATE USER SET\
                        EMAIL = "{}" , PASSWORD = "{}", URL_ID = {}, COMPANY = "{}"\
                        WHERE ID = {};'.format(
                            data.get('EMAIL'),
                            data.get('PASSWORD'),
                            data.get('URL_ID'),
                            data.get('COMPANY'),
                            data.get('ID')
                        ))
        cursor.close()
        self.db.commit()
        print('update query')

    def delete_query(self, id):
        cursor = self.db.cursor()
        cursor.execute(f'DELETE FROM USER WHERE ID = {id};')
        cursor.close()
        self.db.commit()
        print('perform delete')