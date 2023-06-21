
from models.product import ProductModel, StockLocationModel

from models.location import LocationModel, CompanyModel


class Refresh():
    def __init__(self, db= None, api= None):
        
        self.api= api
        self.db= db
        self.product_model= ProductModel(db=db)
        self.location_model= LocationModel(db=db)
        self.company_model= CompanyModel(db=db)
        self.stock_location_model = StockLocationModel(db=db)

    def refresh(self):
        self.stock_location_model.delete_all()
        self.refresh_location()
        self.refresh_product()

    def refresh_location(self):
        # get stock location from odoo api
        stock_location = self.api.get_locations(['id','location_id' , 'company_id', 'display_name'])
    
        # get all stock location ids from sqlite database
        db_ids= self.location_model.select_query(columns=['odoo_id'])

        db_ids_dict = {}
        db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # string have all
        stock_location_ids = ''
        for rec in stock_location:
            stock_location_ids += str(rec['id'])+','
            data = {}
            if not db_ids_dict.get(str(rec['id'])):
                company_id = self.company_model.get_company_id(rec['company_id'][0])
                if not company_id:
                    company_data = {'odoo_id': rec['company_id'][0], 'company_name':rec['company_id'][1]}
                    company_id= self.company_model.create_query(company_data)
                else:
                    company_id = company_id[0][0]
                data= {'odoo_id': rec['id'], 'location_name': rec['display_name'], 'company_id': company_id}
                self.location_model.create_query(data)
        stock_location_ids = stock_location_ids[:-1]
        self.location_model.delete_not_in_query(stock_location_ids)


    def refresh_product(self):
        self.product_model.delete_all_query()
        api_products = self.api.get_stockable_product()
        if api_products:
            db_ids = self.product_model.select_query(columns=['odoo_id'])
            db_ids_dict = {}
            for id in db_ids:
                db_ids_dict[str(id[0])]= 1
            print(db_ids)
            # to verify
            # string have all product in coming from odoo api
            product_ids = ''

            for rec in api_products:
                print(rec)
                product_ids += str(rec['id'])+','
                data = {}
                #check if the product note in the database then add it
                if not db_ids_dict.get(str(rec['id'])):
                    data = {'odoo_id': rec['id'], 'product_name': rec['name'], 'tracking': rec['tracking']}
                    product_id = self.product_model.create_query(data)
                    if rec.get('location_id'):
                        for location, quantity in zip(rec.get('location_id'), rec.get('quantity')):
                            location_id = self.location_model.get_location_id(location)
                            data = {'location_id': location_id[0][0],
                                    'product_id':product_id, 'quantity': quantity}
                            self.stock_location_model.create_query(data)
                else:
                    
                    for add_location in rec.get('location_id'):
                        quantity= rec.get('quantity')[rec.get('location_id').index(add_location)]
                        print(self.api.server_id)
                        print(rec)
                        db_product_id = self.product_model.select_query(columns=['id'], conditions={'odoo_id': rec.get('id')})
                        db_location_id = self.location_model.select_query(columns=['id'], conditions={'odoo_id': add_location})
                        
                        print(db_location_id)
                        print(db_product_id)
                        data = {'location_id': db_location_id[0][0], 'product_id':db_product_id[0][0],
                                'quantity': quantity}
                        self.stock_location_model.create_query(data)
                        print('add location to product')
            
            product_ids = product_ids[:-1]
            self.product_model.delete_not_in_query(product_ids)
            print('finish refreshing product')