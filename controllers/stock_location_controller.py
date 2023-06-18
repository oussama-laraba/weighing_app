import sys

# setting path
sys.path.append('../weighing')
from views.stock_location_view import StockLocationView
from models.stock_location import StockLocationModel



class StockLocationController():
    def __init__(self, view_master= None, db=None, api=None, columns= None, refresh_db_function= None):
        self.columns= columns
        self.model= StockLocationModel(db=db)
        self.api = api
        self.view_master= view_master
        self.stock_location_frame = self.get_view()
        self.refresh_db_function = refresh_db_function


    def create(self, data):
        id = self.model.create_query(data)
        keys = list(data.keys())
        for key in keys:
            data[key.casefold()]= data.get(key)
            data.pop(key)

        data['id'] = id
        color, bg_color = ('green','#e0e0e0') if len(self.user_frame.user_list.frame_list)%2 == 1 else ('blue violet','#C0C0C0')

        self.stock_location_frame.stock_location_list.create_elements(data, color, bg_color)


    def get_view(self):
        stock_location_view = StockLocationView(master=self.view_master, fg_color='white')
        stock_location_view.refresh_button.configure(command=self.refresh)
        self.initialize_view(stock_location_view)
        return stock_location_view
        
    
    def refresh(self):
        self.refresh_db_function()
        self.initialize_view(self.stock_location_frame)


    def initialize_view(self, stock_location_view):
        for rec in stock_location_view.stock_location_list.frame_list:
            rec.destroy()
        stock_location_view.stock_location_list.frame_list = []
        data = self.model.get_data()
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'ODOO_ID': instance[1], 'LOCATION':instance[2], 'COMPANY_ID':instance[3]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            stock_location_view.stock_location_list.create_elements(instance_dict, color, fg_color)