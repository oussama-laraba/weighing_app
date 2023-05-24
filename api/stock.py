import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import OdooStockapi 

url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'
# connection = OdooConnection(url, db, user, key
# ​

def api_connection():
    return OdooStockapi(url, db, user, key)
    

def get_stock_location(fields = [] ):
    connection = api_connection()
    internal_location_ids = connection.get_stock_locations(fields)
    return internal_location_ids


def get_stockable_product(fileds = [] ):
    connection = api_connection()
    stockable_products = connection.get_stockable_products(fileds)
    product_dict = {}
    product_list = []
    for product in stockable_products:
        product_dict.update({str(product['id']): product['name']})
        product_list.append({'id':product['id'], 'name': product['name']})
        print(product['location_id'])


    return product_list
