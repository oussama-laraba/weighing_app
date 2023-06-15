

class StockLocationModel():

    def __init__(self, db=None):
        self.db = db

    def get_data(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM STOCK_LOCATION;')
        stock_location = cursor.fetchall()
        cursor.close()
        return stock_location
    
    def select_query(self, columns='*', conditions= None):
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM STOCK_LOCATION'
        
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0].upper()+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'

        data = cursor.execute(query).fetchall()
        cursor.close()
        return data
        

    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO STOCK_LOCATION (ODOO_ID, LOCATION, COMPANY_ID)\
                                VALUES ({},"{}","{}");'.format(data['ODOO_ID'], data['LOCATION'], data['COMPANY_ID'][1])
        id = cursor.execute(create_query).lastrowid
        self.db.commit()
        cursor.close()
        return id

    def delete_query(self, ids):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM STOCK_LOCATION\
                        WHERE ODOO_ID NOT IN ('+ids+');'

        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()