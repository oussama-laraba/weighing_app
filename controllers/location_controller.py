import sys

# setting path
sys.path.append('../weighing')
from views.location_view import LocationView
from models.location import LocationModel



class LocationController():
    def __init__(self, view_master= None, db=None, api=None, columns= None, refresh_db_function= None):
        self.columns= columns
        self.model= LocationModel(db=db)
        self.api = api
        self.view_master= view_master
        self.stock_location_frame = self.get_view()
        self.refresh_db_function = refresh_db_function


    def create(self, data):
        id = self.model.create_query(data)

        data['id'] = id
        color, bg_color = ('green','#e0e0e0') if len(self.user_frame.user_list.frame_list)%2 == 1 else ('blue violet','#C0C0C0')

        self.stock_location_frame.stock_location_list.create_elements(data, color, bg_color)


    def get_view(self):
        stock_location_view = LocationView(master=self.view_master, fg_color='white')
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
        print('\n\n\n\n',self.api.server_id)
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'id_odoo': instance[1], 'emplacement':instance[2], 'entreprise':instance[3]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            stock_location_view.stock_location_list.create_elements(instance_dict, color, fg_color)