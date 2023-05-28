from odoo_api import *

url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'
# connection = OdooConnection(url, db, user, key)

connection = OdooStockapi(url, db, user, key)
print(connection.get_stockable_products_ids(),'\n')
print(connection.get_stockable_products_records(['barcode']))
# 