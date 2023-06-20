

class  ProductModel():
    def __init__(self, db=None):
        self.db = db


    def get_data(self, location_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM product AS P\
                        INNER JOIN stock_location AS SL ON P.id = SL.PRODUCT_ID\
                        INNER JOIN location AS L ON SL.location_id = L.id AND\
                        L.odoo_id = {};'.format(location_id))
        records= cursor.fetchall()
        cursor.close()
        return records


    # def get_product_locations(self, product_odoo_id):
    #     cursor = self.db.cursor()
    #     select_query = 'SELECT SL.ODOO_ID FROM PRODUCT AS P\
    #                     INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID AND P.ODOO_ID = {}\
    #                     INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
    #                     ;'.format(product_odoo_id)
    #     cursor.execute(select_query)
    #     records = cursor.fetchall()
    #     self.db.commit()
    #     cursor.close()
    #     return records


    def select_query(self, columns='*', conditions= None):
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

        cursor.execute(query)
        records= cursor.fetchall()
        cursor.close()
        return records


    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO product (odoo_id, product_name ,tracking )\
                                VALUES ("{}","{}","{}");'.format(data['odoo_id'], data['product_name'], data['tracking'])
        cursor.execute(create_query)
        id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id


    def delete_not_in_query(self, ids):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM product\
                        WHERE odoo_id NOT IN ('+ids+');'
        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()


    def delete_all_query(self):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM PRODUCT;'
        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()


class UomModel():
    def __init__(self, db=None):
        self.db = db


    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO uom (uom_name)\
                                VALUES ({},"{}")'.format(data['uom_name'].lower())
        cursor.execute(create_query)
        id= cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id
    
    def get_uom_id(self, uom_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM uom WHERE uom_name = {};'.format(uom_name.lower()))
        id = cursor.fetchall()[0][0]
        cursor.close()
        return id
    

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
        
        delete_query = 'DELETE FROM PRODUCT'
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






class StockLocationModel():
    def __init__(self, db=None):
        self.db = db


    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO stock_location (server_id, location_id, product_id, quantity)\
                                VALUES ({},{},{},{})'.format(data['server_id'],  data['location_id'], data['product_id'], data['quantity'])
        
        cursor.execute(create_query)
        id= cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id

    def get_product_locations(self, product_odoo_id):
        cursor = self.db.cursor()
        select_query = 'SELECT L.odoo_id  FROM stock_location as SL\
                        INNER JOIN product AS P ON P.id = SL.product_id AND P.odoo_id = {}\
                        INNER JOIN location AS L ON L.id = SL.location_id\
                        ;'.format(product_odoo_id)
        
        print(select_query)
        cursor.execute(select_query)
        records = cursor.fetchall()
        self.db.commit()
        cursor.close()
        return records
    

    def delete(self, product_odoo_id, location_odoo_id, server_id):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM stock_location AS SL\
                        INNER JOIN product AS P ON SL.product_id = P.id AND P.odoo_id = {}\
                        INNER JOIN location AS L ON L.id = SL.location_id AND L.odoo_id = {} AND SL.server_id = {}\
                        ;'.format(product_odoo_id, location_odoo_id, server_id)
        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()


    def delete_all(self):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM stock_location;')
        self.db.commit()
        cursor.close()
