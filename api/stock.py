import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import *
from models.database_connection import DbConnection


# url = 'http://192.168.1.98:8069'
# db = 'bilbao_test_2'
# user = 'admin@dzexpert.com'
# key = '9691c22a00c554bb26586520ef7f19669583e2d9'
#'36984191bd820a2c86bfda3284a2beb3a40d7a26'
database = DbConnection().db


class ApiConnection():

    def __init__(self):
        self.api_connection = self.connect_api()
        pass

    def connect_api(self):

        cursor = database.cursor()
        cursor.execute('SELECT S.*, U.EMAIL FROM SERVER AS S, USER AS U\
                        WHERE U.URL_ID = S.ID')
        possible_connection = cursor.fetchall()
        for connection in possible_connection:
            url  = connection[1]+':'+str(connection[2])
            db =  connection[3]
            key = connection[4]
            user = connection[5]
            print(url+' '+db+' '+key+' '+user)
            try:
                con = OdooStockapi(url, db, user, key)
                return con    
            except OSError : 
                print("odoo server connection problem")
            
        return None


    def get_locations(self, fields = []):
        try:
            return self.api_connection.get_internal_locations_records(fields)
        except:
            print('Access Denied')
        return None


    def get_stockable_product(self, fields = [] ):

        try: 
            stockable_products = self.api_connection.get_stockable_products_records(fields=['id','name'])
            product_location = self.api_connection.get_stock_locations(fields = ['id','location_id','product_id','quantity','product_uom_id','company_id'])
            product_loc = {}
            for loc in product_location:

                if product_loc.get(loc['product_id'][0]):
                    product_loc[loc['product_id'][0]].append(loc['location_id'][0])
                else:
                    product_loc[loc['product_id'][0]] =  [loc['location_id'][0]]


            product_dict = {}
            product_list = []
            for product in stockable_products:
                product_dict.update({str(product['id']): product['name']})
                product_list.append({'id': product['id'], 'name': product['name'], 'location_id': product_loc.get(product['id'])})

            return product_list
        except: 
            print('Access Denied')

        return None


    def main_product_stock(self, location_id = None):

        try:
            products = self.api_connection.get_stock_locations(fields = ['location_id','product_id','quantity', 'product_uom_id'])
            filtered_products = list()

            for product in list(products):
                if product['location_id'][0] == location_id :
                    del product['id']
                    del product['location_id']
                    filtered_products.append(product)
            return filtered_products

        except:
            print('Access Denied')

        return None

