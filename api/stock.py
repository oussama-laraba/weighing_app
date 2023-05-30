import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import *
from models.database_connection import database_connection


url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'
#'36984191bd820a2c86bfda3284a2beb3a40d7a26'

# connection = OdooConnection(url, db, user, key
database = database_connection()

def api_connection():

    cursor = database.cursor()
    cursor.execute('SELECT S.*, U.EMAIL FROM SERVER AS S, USER AS U\
                    WHERE U.URL_ID = S.ID')
    possible_connection = cursor.fetchall()
    print(possible_connection)
    for connection in possible_connection:
        url  = connection[1]+':'+str(connection[2])
        db =  connection[3]
        key = connection[4]
        user = connection[5]

        try:
            con = OdooStockapi(url, db, user, key)
            return con    
        except OSError : 
            print("odoo server connection problem")
        
        
    return None
    


def get_locations(fields = []):
    connection = api_connection()
    try:
        return connection.get_internal_locations_records(fields)
    except:
        print('Access Denied')
    return None


def get_stockable_product(fields = [] ):
    connection = api_connection()
    try: 
        stockable_products = connection.get_stockable_products_records(fields=['id','name'])
        product_location = connection.get_stock_locations(fields = ['id','location_id','product_id','quantity','product_uom_id','company_id'])

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


def main_product_stock(location_id = None):
    connection = api_connection()
    try:
        products = connection.get_stock_locations(fields = ['location_id','product_id','quantity', 'product_uom_id'])
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


main_product_stock(8)

# try:
#     con = OdooStockapi(url, db, user, key)
# except OSError : 
#     print("odoo server connection problem")

# try:
#     api_connection()
# except: 
#     print("hello world")
# finally: 
#     print("finish")