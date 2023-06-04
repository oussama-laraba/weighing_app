import sys

# setting path
sys.path.append('../weighing')
from templates.scrollable_list_frame import ScrollableListFrame
from views.stock_location_view import StockLocationView
from models.stock_location import StockLocationModel

from api.stock import get_locations


class StockLocationController():
    def __init__(self, view_master= None, columns= None, db_name= None):

        self.columns= columns
        self.db_name= db_name
        self.model= StockLocationModel()
        self.view_master= view_master
        self.stock_location_frame = self.get_view()
        

    def create(self, data):
        print("create button clicked")
        print(data)
        id = self.model.create_query(data)
        keys = list(data.keys())
        for key in keys:
            data[key.casefold()]= data.get(key)
            data.pop(key)

        data['id'] = id
        print(data)
        color, bg_color = ('green','#e0e0e0') if len(self.user_frame.user_list.frame_list)%2 == 1 else ('blue violet','#C0C0C0')

        self.stock_location_frame.stock_location_list.create_elements(data, color, bg_color)


    def get_view(self):
        stock_location_view = StockLocationView(master=self.view_master, fg_color='white')
        stock_location_view.refresh_button.configure(command=self.refresh)
        self.initialize_view(stock_location_view)
        return stock_location_view
        
    
    def refresh(self):
        print('click refresh')
        
        # get stock location from odoo api
        stock_location = get_locations(['id','location_id' , 'company_id', 'display_name'])
        # get all stock location ids from sqlite database
        db_ids= self.model.select_query(columns=['ODOO_ID'])

        db_ids_dict = {}
        db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # string have all
        stock_location_ids = ''
        for rec in stock_location:
            stock_location_ids += str(rec['id'])+','
            data = {}
            if not db_ids_dict.get(str(rec['id'])):
                data= {'ODOO_ID': rec['id'], 'LOCATION': rec['display_name'], 'COMPANY_ID': rec['company_id']}
                self.model.create_query(data)
        stock_location_ids = stock_location_ids[:-1]
        self.model.delete_query(stock_location_ids)
        self.initialize_view(self.stock_location_frame)
        pass


    def initialize_view(self, stock_location_view):
        for rec in stock_location_view.stock_location_list.frame_list:
            rec.destroy()
        stock_location_view.stock_location_list.frame_list = []
        data = self.model.get_data()
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'ODOO_ID': instance[1], 'LOCATION':instance[2], 'COMPANY_ID':instance[3]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            stock_location_view.stock_location_list.create_elements(instance_dict, color, fg_color)
        #server_view.server_list.server_initialize(data)