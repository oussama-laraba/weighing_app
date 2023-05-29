import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import *

url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'
# connection = OdooConnection(url, db, user, key


def api_connection():
    return OdooStockapi(url, db, user, key)
    


def get_locations(fields = []):
    connection = api_connection()
    internal_location_ids = connection.get_internal_locations_records(fields)
    return internal_location_ids


def get_stockable_product(fields = [] ):
    connection = api_connection()
    stockable_products = connection.get_stockable_products_records(fields=['id','name'])
    product_location = connection.get_stock_locations(fields = ['id','location_id','product_id','quantity','product_uom_id','company_id'])

    print(product_location)

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


connection = api_connection()

def main_product_stock(location_id = None):
    connection = api_connection()
    products = connection.get_stock_locations(fields = ['location_id','product_id','quantity'])
    filtered_products = list()

    for product in list(products):
        print(product['location_id'])
        if product['location_id'][0] == location_id :
            del product['id']
            del product['location_id']
            filtered_products.append(product)
    print(filtered_products)
    return filtered_products

