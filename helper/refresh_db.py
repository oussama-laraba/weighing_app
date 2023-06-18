
from models.product import ProductModel, ProductLocationModel

from models.stock_location import StockLocationModel


class Refresh():
    def __init__(self, db= None, api= None):
        
        self.api= api
        self.db= db
        self.product_model= ProductModel(db=db)
        self.location_model= StockLocationModel(db=db)
        self.product_location_model = ProductLocationModel(db=db)



    def refresh_location(self):
        # get stock location from odoo api
        stock_location = self.api.get_locations(['id','location_id' , 'company_id', 'display_name'])

        # get all stock location ids from sqlite database
        db_ids= self.location_model.select_query(columns=['ODOO_ID'])

        db_ids_dict = {}
        db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # string have all
        stock_location_ids = ''
        for rec in stock_location:
            stock_location_ids += str(rec['id'])+','
            data = {}
            if not db_ids_dict.get(str(rec['id'])):
                data= {'ODOO_ID': rec['id'], 'LOCATION': rec['display_name'], 'COMPANY_ID': rec['company_id']}
                self.location_model.create_query(data)
        stock_location_ids = stock_location_ids[:-1]
        self.location_model.delete_query(stock_location_ids)


    def refresh_product(self):
        api_products = self.api.get_stockable_product()
        if api_products:
            db_ids = self.product_model.select_query(columns=['ODOO_ID'])
            db_ids_dict = {}
            for id in db_ids:
                db_ids_dict[str(id[0])]= 1

            self.product_location_model.delete_all()
            # string have all product in coming from odoo api
            product_ids = ''

            for rec in api_products:
                product_ids += str(rec['id'])+','
                data = {}
                #check if the product note in the database then add it
                if not db_ids_dict.get(str(rec['id'])):
                    data = {'ODOO_ID': rec['id'], 'NAME': rec['name']}
                    product_id = self.product_model.create_query(data)
                    if rec.get('location_id'):
                        for location in rec.get('location_id'):
                            location_id = self.location_model.select_query(columns=['ID'], conditions={'ODOO_ID': location})
                            data = {'STOCK_LOCATION_ID': location_id[0][0], 'PRODUCT_ID':product_id}
                            self.product_location_model.create_query(data)
                else:
                    db_product_location_copy = self.product_model.get_product_locations(rec['id'])
                    db_product_location = list()
                    for location in db_product_location_copy:
                        db_product_location.append(location[0])
                    del db_product_location_copy
                    
                    if rec.get('location_id'): 
                        api_product_location = rec.get('location_id')
                        to_remove_location = list(set(db_product_location)- set(api_product_location))
                        to_add_location = list(set(api_product_location)- set(db_product_location))
                        for rm_location in to_remove_location:
                            self.product_location_model.delete(rec.get('id'), rm_location)

                        for add_location in to_add_location:
                            db_product_id = self.product_model.select_query(columns=['ID'], conditions={'ODOO_ID': rec.get('id')})
                            db_location_id = self.location_model.select_query(columns=['ID'], conditions={'ODOO_ID': add_location})
                            
                            data = {'STOCK_LOCATION_ID': db_location_id[0][0], 'PRODUCT_ID':db_product_id[0][0]}
                            self.product_location_model.create_query(data)
                            print('add location to product')
            
            product_ids = product_ids[:-1]
            self.product_model.delete_not_in_query(product_ids)