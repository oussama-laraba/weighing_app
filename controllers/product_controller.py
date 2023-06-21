import sys

# setting path
sys.path.append('../weighing')

from views.product_view import ProductView
from models.product import ProductModel, StockLocationModel
from models.location import LocationModel



class ProductController():
    def __init__(self, view_master= None, db=None, api=None, columns= None, refresh_db_function=None):
        self.columns= columns
        self.api = api
        self.model= ProductModel(db=db)
        self.location_model = LocationModel(db=db)
        self.stock_location_model = StockLocationModel(db=db)
        self.view_master= view_master
        self.location_values_id = {}
        self.product_frame = self.get_view()
        self.refresh_db_function = refresh_db_function


    def refresh(self):
        self.refresh_db_function()
        self.initialize_view(self.product_frame)


    def location_callback(self, location):
        self.initialize_view(self.product_frame)


    def location_load(self, product_view):
        
        location_id = self.location_model.select_query(columns=['odoo_id','location_name'])
        self.location_values_id = { location[1]:location[0] for location in location_id }
        locations = list(self.location_values_id.keys())
        
        product_view.location.configure(values=locations)
        
        if locations:
            product_view.location.set(locations[0])


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
        
        data = None
        if location_id:
            data = self.model.get_data(location_id)
        if data:
            for idx,instance in enumerate(data):
                instance_dict = {'id': instance[0],'ODOO_ID': instance[1], 'PRODUCT':instance[2], 'type de suivi':instance[3]}
                color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
                product_view.product_list.create_elements(instance_dict, color, fg_color)