

class LocationModel():
    def __init__(self, db=None):
        self.db = db


    def get_data(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT L.id, L.odoo_id, L.location_name, C.company_name FROM location as L\
                       INNER JOIN  company as C ON C.id = L.company_id;')
        stock_location = cursor.fetchall()
        cursor.close()
        return stock_location


    def select_query(self, columns='*', conditions= None):
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM location'
        
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0].upper()+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'

        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records


    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO location (odoo_id, location_name, company_id)\
                                VALUES ({},"{}","{}");'.format(data['odoo_id'], data['location_name'], data['company_id'])
        cursor.execute(create_query)
        id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id


    def delete_query(self, ids):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM location\
                        WHERE ODOO_ID NOT IN ('+ids+');'
        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()


class CompanyModel():
    def __init__(self, db= None):
        self.db = db

    def get_data(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM company;')
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_company_id(self, odoo_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM company WHERE odoo_id = {};'.format(odoo_id))
        id = cursor.fetchall()[0][0]
        cursor.close()
        return id

    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO company (odoo_id, company_name)\
                                VALUES ({},"{}");'.format(data['odoo_id'], data['company_name'])
        cursor.execute(create_query)
        id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return id

    def update_query(self, data):
        cursor = self.db.cursor()
        cursor.execute('UPDATE company SET\
                        company_name = "{}" WHERE ID = {};'.format(
                            data.get('company_name'),
                            data.get('id')
                        ))
        cursor.close()
        self.db.commit()
    
