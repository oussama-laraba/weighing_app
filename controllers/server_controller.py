import sys

# setting path
sys.path.append('../weighing')
from templates.scrollable_list_frame import ScrollableListFrame, DeleteConfirmation
from views.server_view import ServerView, CreateUpdateServer
from models.server import ServerModel


class SeverController():

    def __init__(self, view_master= None, db=None, columns= None, db_name= None):

        self.columns= columns
        self.db_name= db_name
        self.model= ServerModel(db=db)
        self.view_master= view_master
        self.server_frame = self.get_view()
        

    def show_create_edit_window(self, element= None):
        if element:
            CreateUpdateServer(edit=True, server=element, create_edit_function= self.create_edit_frame_button, button= self.edit)
        else:
            CreateUpdateServer(button= self.create, create_edit_function= self.create_edit_frame_button,)

    def create_edit_frame_button(self, element):
        validation_text = self.form_validation(element)
        if not validation_text:
            print('valid')
            data = {}
            
            data['ID'] = element.server.id if element.edit else None
            data['URL'] = element.url.get().strip()
            data['PORT'] = int(element.port.get())
            data['DATABASE'] = element.database.get().strip()
            data['KEY'] = element.key.get().strip()
            element.button(data)

            if element.edit:
                element.server.data_dict.get('url').configure(text = element.url.get())
                element.server.data_dict.get('port').configure(text = element.port.get())
                element.server.data_dict.get('database').configure(text = element.database.get())
                element.server.data_dict.get('key').configure(text = element.key.get())

            element.destroy()
        else: 
            element.button1.grid_forget()
            element.validation_text.configure(text = validation_text)
            element.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            element.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")
    

    def create(self, data):
        id = self.model.create_query(data)
        keys = list(data.keys())
        for key in keys:
            data[key.casefold()]= data.get(key)
            data.pop(key)

        data['id'] = id
        color, bg_color = ('green','#e0e0e0') if len(self.server_frame.server_list.frame_list)%2 == 1 else ('blue violet','#C0C0C0')

        self.server_frame.server_list.create_elements(data, color, bg_color)
        

    def edit(self, data):
        self.model.update_query(data)
        


    def form_validation(self, element):
        if '' in [element.url.get().strip(), element.port.get().strip(), element.database.get().strip(), element.key.get().strip()]:
            return 'Vous devez remplir tous le formulaire'
        
        if not element.port.get().isnumeric():
            return 'Le port doit etre un entier positive'
        
        check_duplicate_condition = {'url': element.url.get().strip(),\
                                    'port': element.port.get().strip(),\
                                    'database': element.database.get().strip(),\
                                    'key': element.key.get().strip(),\
                                    }
        
        records = self.model.select_query(columns=['ID'], conditions = check_duplicate_condition)

        # if the record who have the same conf it's not the same
        if len(records) > 1 or (len(records) == 1 and (element.id,) not in records):
            return 'Cette enregistrement il exist déja '

        return None

    def delete(self, element):
        DeleteConfirmation(element, self.delete_confirmation)

    def delete_confirmation(self, element):
        self.model.delete_query(element.id)
        self.server_frame.server_list.frame_list = list(filter(lambda x: x.id != element.id, self.server_frame.server_list.frame_list))
        element.destroy()        

    def get_view(self):
        buttons = {'edit': self.show_create_edit_window, 'delete': self.delete}
        server_view = ServerView(master=self.view_master, fg_color='white',buttons=buttons)
        server_view.add_button.configure(command=self.show_create_edit_window)
        self.initialize_view(server_view)
        return server_view
        

    def initialize_view(self, server_view):
        data = self.model.select_query('*')
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'url': instance[1], 'port':instance[2], 'database':instance[3], 'key': instance[4]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            server_view.server_list.create_elements(instance_dict, color, fg_color)
        #server_view.server_list.server_initialize(data)