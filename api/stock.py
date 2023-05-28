import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import *

url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'
# connection = OdooConnection(url, db, user, key
# ​

def api_connection():
    return OdooStockapi(url, db, user, key)
    

def get_stock_location(fields = []):
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



connection = api_connection()
product_dict = {}
print(connection.get_stockable_products_ids(query = [['detailed_type','=','product'] , ['barcode','!=' , False]]))
stock_location= get_stock_location()
# print(connection.get_internal_locations_records( ['id','display_name','name']))



# print(get_stock_location())
# print(stock_location[0][0])

#print(f'\nFirst Two stock locations:\n {internal_location_ids} \n\n')



# stockable_products = connection.get_stockable_products()​
# stockable_products_keys = (list (stockable_products[0]))[0:7]
# stockable_product_1 = stockable_products[0]
# stockable_product_1_limited_cols = {key: stockable_product_1[key] for key in stockable_products_keys }
# print(stockable_product_1_limited_cols, '\n\n')
# print('\n\n',stockable_products, '\n\n')
# val_dict = {  'product_id': 8 , 'product_qty':20, 'company_id':1}
# connection.create_product_lot(val_dict)