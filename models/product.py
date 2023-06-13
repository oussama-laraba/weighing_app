

class  ProductModel():

    def __init__(self, db=None):
        self.db = db


    def get_data(self, location_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM PRODUCT AS P\
                        INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
                        INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID AND\
                        SL.ODOO_ID = {};'.format(location_id))
        
        return cursor.fetchall()
    


    def get_product_locations(self, product_odoo_id):
        cursor = self.db.cursor()
        select_query = 'SELECT SL.ODOO_ID FROM PRODUCT AS P\
                        INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID AND P.ODOO_ID = {}\
                        INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
                        ;'.format(product_odoo_id)
        stock_locations_ids = cursor.execute(select_query).fetchall()
        self.db.commit()
        cursor.close()
        return stock_locations_ids


    def select_query(self, columns='*', conditions= None):
        print("perform query select")
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM PRODUCT'
        
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
        create_query = 'INSERT INTO PRODUCT (ODOO_ID, NAME)\
                                VALUES ("{}","{}");'.format(data['ODOO_ID'], data['NAME'])
        print(create_query)
        id = cursor.execute(create_query).lastrowid
        print("hello")
        self.db.commit()
        cursor.close()
        return id

    def update_query(self, data):
        
        print('update query')

    def delete_not_in_query(self, ids):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM PRODUCT\
                        WHERE ODOO_ID NOT IN ('+ids+');'

        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()
        print('perform delete')

    def delete_all_query(self):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM PRODUCT;'

        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()
        print('perform delete')






class ProductLocationModel():
    def __init__(self, db=None):
        self.db = db


    def create_query(self, data):
        cursor = self.db.cursor()
        print(data)
        create_query = 'INSERT INTO PRODUCT_LOCATION (STOCK_LOCATION_ID, PRODUCT_ID)\
                                VALUES ({},"{}")'.format(data['STOCK_LOCATION_ID'], data['PRODUCT_ID'])
        id = cursor.execute(create_query).lastrowid
        self.db.commit()
        cursor.close()
        return id

    def delete(self, product_odoo_id, location_odoo_id):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM PRODUCT_LOCATION AS PL\
                        INNER JOIN PRODUCT AS P ON PL.PRODUCT_ID = P.ID AND P.ODOO_ID = {}\
                        INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID AND SL.ODOO_ID = {}\
                        ;'.format(product_odoo_id, location_odoo_id)
        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()

    def delete_all(self):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM PRODUCT_LOCATION;')
        self.db.commit()
        cursor.close()