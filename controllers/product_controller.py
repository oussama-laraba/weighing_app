import sys

# setting path
sys.path.append('../weighing')
from templates.scrollable_list_frame import ScrollableListFrame
from views.product_view import ProductView
from models.product import ProductModel, ProductLocationModel

from models.stock_location import StockLocationModel

from api.stock import ApiConnection


class ProductController():
    def __init__(self, view_master= None, db=None, columns= None, db_name= None):

        self.columns= columns
        self.db_name= db_name
        self.api_connection = ApiConnection()
        self.model= ProductModel(db=db)
        self.stock_location_model = StockLocationModel(db=db)
        self.product_location_model = ProductLocationModel(db=db)
        self.view_master= view_master
        self.location_values_id = {}
        self.product_frame = self.get_view()


    def refresh(self):
        api_products = self.api_connection.get_stockable_product()

        if api_products:
            db_ids = self.model.select_query(columns=['ODOO_ID'])
            #self.model.delete_all_query()
            db_ids_dict = {}
            for id in db_ids:
                db_ids_dict[str(id[0])]= 1
            #db_ids = list(map(lambda x: db_ids_dict[str(x[0])]= 1, db_ids))
            
            print(db_ids)
            self.product_location_model.delete_all()
            # string have all
            product_ids = ''

            for rec in api_products:
                
                data = {}
                if not db_ids_dict.get(str(rec['id'])):
                    data = {'ODOO_ID': rec['id'], 'NAME': rec['name']}
                    product_id = self.model.create_query(data)
                    print(rec)
                    if rec.get('location_id'):
                        for location in rec.get('location_id'):
                            location_id = self.stock_location_model.select_query(columns=['ID'], conditions={'ODOO_ID': location})
                            data = {'STOCK_LOCATION_ID': location_id[0][0], 'PRODUCT_ID':product_id}
                            self.product_location_model.create_query(data)
                            print('add product')
                else: product_ids += str(rec['id'])+','
            product_ids = product_ids[:-1]
            print('\n\n\n\n\n')
            print(product_ids)
            # self.model.delete_query(product_ids)
            self.initialize_view(self.product_frame)
    


        # # get stock location from odoo api
        # stock_location = get_locations(['id','location_id' , 'company_id', 'display_name'])
        # # get all stock location ids from sqlite database
        # db_ids= self.model.select_query(columns=['ODOO_ID'])

        # db_ids_dict = {}
        # db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # # string have all
        # stock_location_ids = ''
        # for rec in stock_location:
        #     stock_location_ids += str(rec['id'])+','
        #     data = {}
        #     if not db_ids_dict.get(str(rec['id'])):
        #         data= {'ODOO_ID': rec['id'], 'LOCATION': rec['display_name'], 'COMPANY_ID': rec['company_id']}
        #         self.model.create_query(data)
        # stock_location_ids = stock_location_ids[:-1]
        # self.model.delete_query(stock_location_ids)
        # self.initialize_view(self.stock_location_frame)
        pass
        
    def location_callback(self, location):
        print(location)
        self.initialize_view(self.product_frame)
        pass

    def location_load(self, product_view):

        location_id = self.stock_location_model.select_query(columns=['ODOO_ID','LOCATION'])
        self.location_values_id = { location[1]:location[0] for location in location_id }
        locations = list(self.location_values_id.keys())
        product_view.location.configure(values=locations)
        product_view.location.set(locations[0])

        pass


    def get_view(self):
        product_view = ProductView(master=self.view_master, fg_color='white')
        product_view.refresh_button.configure(command=self.refresh)
        self.location_load(product_view)
        product_view.location.configure(command=self.location_callback)
        self.initialize_view(product_view)
        return product_view


    def initialize_view(self, product_view):
        for rec in product_view.product_list.frame_list:
            rec.destroy()
        product_view.product_list.frame_list = []

        location_id = self.location_values_id.get(product_view.location.get())
        data = self.model.get_data(location_id)
        print(location_id)
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'ODOO_ID': instance[1], 'PRODUCT':instance[2]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            product_view.product_list.create_elements(instance_dict, color, fg_color)
        #server_view.server_list.server_initialize(data)