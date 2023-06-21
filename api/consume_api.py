import sys

# setting path
sys.path.append('../weighing')

from api.odoo_api import *



# url = 'http://192.168.1.98:8069'
# db = 'bilbao_test_2'
# user = 'admin@dzexpert.com'
# key = '9691c22a00c554bb26586520ef7f19669583e2d9'
#'36984191bd820a2c86bfda3284a2beb3a40d7a26'
# database = DbConnection().db


class ApiConnection():

    def __init__(self, db=None):
        self.db = db
        self.user_id= None
        self.server_id= None
        self.api_connection = self.connect_api()


    def connect_api(self):
        print('api connection')
        cursor = self.db.cursor()
        cursor.execute('SELECT S.*, U.id, U.email, U.password FROM server AS S, user AS U\
                        WHERE U.server_id = S.id')
        possible_connection = cursor.fetchall()
        cursor.close()
        for connection in possible_connection:
            url  = connection[1]+':'+str(connection[2])
            db =  connection[3]
            #key = connection[4]
            key= connection[-1]
            user = connection[5]

            try:
                con = OdooStockapi(url, db, user, key)
                self.server_id = connection[0]
                self.user_id = connection[4]
                return con    
            except OSError : 
                print("odoo server connection problem")
        print('cannot connect')
        
        return None


    def get_locations(self, fields = []):
        print('api call get_locations')
        try:
            return self.api_connection.get_internal_locations_records(fields)
        except:
            print('Access Denied')
        return None


    def get_stockable_product(self, fields = [], location_id= None ):

        print('api call get_stockable_product')
        try: 
        # try: 
            stockable_products = con.get_stockable_products_records(fields=['id','name','uom_id','tracking'])
            product_location = con.get_stock_locations()
            
            product_loc = {}
            for loc in product_location:
                
                if product_loc.get(loc['product_id'][0]):
                    if loc['location_id'][0] in product_loc[loc['product_id'][0]]['location_id']:
                        if loc.get('lot_id'):
                            product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] +=  loc['quantity']
                        else: 
                            product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] +=  loc['quantity']
                    else:
                        product_loc[loc['product_id'][0]]['location_id'].append(loc['location_id'][0])
                        product_loc[loc['product_id'][0]]['quantity'][loc['location_id'][0]] = {'total_quantity':0, 'to_use_quantity':0}

                        if loc.get('lot_id'):
                            product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] =  loc['quantity']
                        else: 
                            product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] =  loc['quantity']
                else:
                    product_loc[loc['product_id'][0]]= {}
                    product_loc[loc['product_id'][0]]['location_id'] =  [loc['location_id'][0]]
                    product_loc[loc['product_id'][0]]['quantity'] = {loc['location_id'][0]:{'total_quantity':0, 'to_use_quantity':0}}

                    if loc.get('lot_id'):
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] =  loc['quantity']
                    else:
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] =  loc['quantity']

            product_dict = {}
            product_list = []
            for product in stockable_products:

                if product_loc.get(product['id']):
                    product_dict.update({str(product['id']): product['name']})
                    product_list.append({'id': product['id'], 'name': product['name'], 'location_id': product_loc.get(product['id']).get('location_id'),
                                        'quantity':product_loc.get(product['id']).get('quantity'),
                                        'uom_id':product.get('uom_id')[1],
                                        'tracking':product.get('tracking')})
                else:
                    product_list.append({'id': product['id'], 'name': product['name'], 'location_id': [],
                                        'quantity':None, 'uom_id':product.get('uom_id')[1],
                                        'tracking':product.get('tracking')})
            
            if location_id:
                product_list_copy = list(product_list)
                for product in product_list_copy:
                    if location_id in product.get('location_id'):
                        product['quantity'] = product.get('quantity').get(location_id)
                        product['location_id'] = location_id
                    else:
                        product_list.remove(product)
            return product_list
        except: 
            print('Access Denied')

        return None


    def main_product_stock(self, location_id = None):
        print('api call main_product_stock')
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

    def create_code_bar(self, barcode_information):
        print(barcode_information)
        print('\n\n\n\n\n')
        new_lot = self.api_connection.create(
            'erpish.product.quant.create.codebar',
            barcode_information
        )
        print('create lot')
        print('\n\n\n\n\n')
        #new_lot.action_create()
        barcode = self.api_connection.call_method(
            'erpish.product.quant.create.codebar',
            'action_create',
            [new_lot]
        )
        print('create barcode')
        print(barcode)

        return barcode


def check_connection(data):
    try:
        con = OdooStockapi(data.get('url'), data.get('db'), data.get('user'), data.get('key'))
        return con.state()
    
    except:
        return None
    

def create_code_bar(con, barcode_information):
        print(barcode_information)
        print('\n\n\n\n\n')
        new_lot = con.create(
            'erpish.product.quant.create.codebar',
            barcode_information
        )
        print('create lot')
        print('\n\n\n\n\n')
        
        barcode = con.call_method(
            'erpish.product.quant.create.codebar',
            'action_create',
            [new_lot]
        )
        print('create barcode')
        print(barcode)

        return barcode

# def main_product_stock(con, location_id = None):

#         try:
#             products = con.get_stock_locations(fields = ['location_id','product_id','quantity', 'product_uom_id'])
#             filtered_products = list()
#             for product in list(products):
#                 if product['location_id'][0] == location_id :
#                     del product['id']
#                     del product['location_id']
#                     filtered_products.append(product)

#             return filtered_products

#         except:
#             print('Access Denied')

#         return None


def get_stockable_product(con, fields = [], location_id=None):


        print('api call get_stockable_product')
        # try: 
        stockable_products = con.get_stockable_products_records(fields=['id','name','uom_id','tracking'])
        product_location = con.get_stock_locations()
        
        product_loc = {}
        for loc in product_location:
            
            if product_loc.get(loc['product_id'][0]):
                if loc['location_id'][0] in product_loc[loc['product_id'][0]]['location_id']:
                    if loc.get('lot_id'):
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] +=  loc['quantity']
                    else: 
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] +=  loc['quantity']
                else:
                    product_loc[loc['product_id'][0]]['location_id'].append(loc['location_id'][0])
                    product_loc[loc['product_id'][0]]['quantity'][loc['location_id'][0]] = {'total_quantity':0, 'to_use_quantity':0}

                    if loc.get('lot_id'):
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] =  loc['quantity']
                    else: 
                        product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] =  loc['quantity']
            else:
                product_loc[loc['product_id'][0]]= {}
                product_loc[loc['product_id'][0]]['location_id'] =  [loc['location_id'][0]]
                product_loc[loc['product_id'][0]]['quantity'] = {loc['location_id'][0]:{'total_quantity':0, 'to_use_quantity':0}}

                if loc.get('lot_id'):
                    product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['total_quantity'] =  loc['quantity']
                else:
                    product_loc[loc['product_id'][0]]['quantity'].get(loc['location_id'][0])['to_use_quantity'] =  loc['quantity']

        product_dict = {}
        product_list = []
        for product in stockable_products:

            if product_loc.get(product['id']):
                product_dict.update({str(product['id']): product['name']})
                product_list.append({'id': product['id'], 'name': product['name'], 'location_id': product_loc.get(product['id']).get('location_id'),
                                    'quantity':product_loc.get(product['id']).get('quantity'),
                                    'uom_id':product.get('uom_id')[1],
                                    'tracking':product.get('tracking')})
            else:
                product_list.append({'id': product['id'], 'name': product['name'], 'location_id': [],
                                    'quantity':None, 'uom_id':product.get('uom_id')[1],
                                    'tracking':product.get('tracking')})
        
        if location_id:
            product_list_copy = list(product_list)
            for product in product_list_copy:
                if location_id in product.get('location_id'):
                    product['quantity'] = product.get('quantity').get(location_id)
                    product['location_id'] = location_id
                else:
                    product_list.remove(product)
        return product_list
        # except: 
        #     print('Access Denied')

        return None
def main_product_stock(con, location_id = None):
    print('api call main_product_stock')
    try:
        products = con.get_stock_locations(fields = ['location_id','product_id','quantity', 'product_uom_id'])
        filtered_products = list()

        for product in list(products):
            if product['location_id'][0] == location_id :
                del product['id']
                del product['location_id']
                filtered_products.append(product)
        print(filtered_products)
        return filtered_products

    except:
        print('Access Denied')

    return None

# url  = 'http://demo.dzexpert.com'+':8069'
# db =  'ODOO11_TEST'

url  = 'http://192.168.1.160'+':8069'
db =  'recouverement_test'

# url = 'http://192.168.1.98'+':8069'
# db =  'bilbao_test_2'
key= '123456'
# user = 'admin@dzexpert.com'
user = 'admin@t.com'

# print('\n\n\n\n')
# print(len(key))
# print(url+' '+db+' '+user+' '+key)
# print('\n\n\n\n')




# create_code_bar(con,{'product_id': 4, 'location_id': 12, 'quantity': 6.0, 'quantity2': 6.0, 'information': 'text info\n'})
con = OdooStockapi(url, db, user, key)
get_stockable_product(con, location_id=12)
# # print(con.get_stock_locations(location_id=126))

# print('\n\n\n\n')
# print(main_product_stock(con,12))

# #print(con.get_internal_locations_ids())
# main_product_stock(con,12)
# print(con.get_records(  'product.product', con.get_ids('product.product'))[0])