import sys
sys.path.append('../weighing')
from views.lot_view import LotView
from models.lot import LotModel
from models.stock_location import StockLocationModel
from models.product import ProductModel


class LotController():
    def __init__(self, view_master= None, db=None, api=None, columns= None, refresh_db_function= None):
        self.columns= columns
        self.model= LotModel(db=db)
        self.api = api
        self.stock_location_model= StockLocationModel(db=db)
        self.product_model= ProductModel(db=db)
        self.view_master= view_master
        self.location_values_id = {}
        self.product_values_id = {}
        self.lot_frame = self.get_view()
        self.refresh_db_function = refresh_db_function


    def refresh(self):
        print('button refresh pressed')
        pass


    def search(self):
        print('button search pressed')
        pass


    def location_load(self, lot_view):
        location_id = self.stock_location_model.select_query(columns=['ODOO_ID','LOCATION'])
        self.location_values_id = { location[1]:location[0] for location in location_id }
        locations = list(self.location_values_id.keys())
        
        lot_view.location.configure(values=locations)
        
        if locations:
            lot_view.location.set(locations[0])


    def location_callback(self, location):
        print(location)
        #self.initialize_view(self.product_frame)

    def get_view(self):
        lot_view = LotView(master=self.view_master, fg_color='white')
        lot_view.refresh_button.configure(command=self.refresh)
        lot_view.search_button.configure(command=self.search)
        
        self.location_load(lot_view)
        lot_view.location.configure(command=self.location_callback)
        #self.initialize_view(lot_view)
        return lot_view