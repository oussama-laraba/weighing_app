
class UserModel():
    def __init__(self, db=None):
        self.db = db


    def get_data(self):
        cursor = self.db.cursor()
        
        cursor.execute('SELECT U.id, U.email, U.password, S.url\
                        FROM user as U\
                        INNER JOIN  server as S ON U.server_id = S.id')
        records = cursor.fetchall()
        cursor.close()
        return records


    def select_query(self, columns='*', conditions= None):
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM user'
        
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0].upper()+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'
        cursor.execute(query)
        records= cursor.fetchall()
        cursor.close()
        return records


    def create_query(self, data):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO user \
                    (email, password, server_id)\
                    VALUES ("{}", "{}", "{}");'.format(
                        data.get('email'),
                        data.get('password'),
                        data.get('server_id')
                    ))
        id = cursor.lastrowid
        cursor.close()
        self.db.commit()
        return id


    def update_query(self, data):
        cursor = self.db.cursor()
        cursor.execute('UPDATE user SET\
                        email = "{}" , password = "{}", server_id = {}\
                        WHERE id = {};'.format(
                            data.get('email'),
                            data.get('password'),
                            data.get('server_id'),
                            data.get('id')
                        ))
        print('user update')
        cursor.close()
        self.db.commit()


    def delete_query(self, id):
        cursor = self.db.cursor()
        cursor.execute(f'DELETE FROM user WHERE id = {id};')
        cursor.close()
        self.db.commit()



class ProductUomModel():
    def __init__(self, db=None):
        self.db = db


    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO product_uom (product_id, uom_id)\
                                VALUES ({},"{}")'.format(data['product_id'],data['uom_id'])
        cursor.execute(create_query)
        id= cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id
    
    def delete_query(self, conditions= None):
        cursor = self.db.cursor()
        
        delete_query = 'DELETE FROM product'
        if conditions:
            delete_query+= ' WHERE'
            for condition in conditions.items():
                delete_query+= '  '+condition[0]+' = "'+condition[1]+'" AND'
            delete_query= delete_query[:-3]
        delete_query+=';'

        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()
        return None


    def get_uom_id(self, uom_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM uom WHERE uom_name = {};'.format(uom_name.lower()))
        id = cursor.fetchall()[0][0]
        cursor.close()
        return id