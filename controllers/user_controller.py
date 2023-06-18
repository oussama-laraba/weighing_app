import sys

# setting path
sys.path.append('../weighing')
from templates.scrollable_list_frame import  DeleteConfirmation
from views.user_view import UserView, CreateUpdateUser
from models.user import UserModel
from models.server import ServerModel
from api.stock import check_connection


class UserController():
    def __init__(self, view_master= None, db=None, columns= None, db_name= None):
        self.columns= columns
        self.db_name= db_name
        self.model= UserModel(db=db)
        self.server_model= ServerModel(db=db)
        self.view_master= view_master
        self.user_frame = self.get_view()


    def show_create_edit_window(self, element= None):
        if element:
            CreateUpdateUser(server_model= self.server_model, user=element, button= self.edit, create_edit_function= self.create_edit_button)
        else:
            CreateUpdateUser(server_model= self.server_model, button= self.create, create_edit_function= self.create_edit_button)


    def create_edit_button(self, element):
        validation_text = self.form_validation(element)
        if not validation_text:
            data = {}
            data['ID'] = element.user.id if element.user else None
            data['EMAIL'] = element.email.get().strip()
            data['PASSWORD'] = element.password.get().strip()
            data['URL_ID'] = int(element.url_id)
            data['COMPANY'] = element.company.get().strip()
            element.button(data)

            if element.user:
                element.user.data_dict.get('email').configure(text = element.email.get())
                element.user.data_dict.get('password').configure(text = ''.join('*' for _ in range(len(element.password.get()))))
                element.user.data_dict.get('url_id').configure(text = element.url_names.get())
                element.user.data_dict.get('company').configure(text = element.company.get())
            
            element.destroy()
            self.view_master.api.api_connection = self.view_master.api.connect_api()
            self.view_master.refresher.refresh_location()
            self.view_master.refresher.refresh_product()
        
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
        color, bg_color = ('green','#e0e0e0') if len(self.user_frame.user_list.frame_list)%2 == 1 else ('blue violet','#C0C0C0')
        self.user_frame.user_list.create_elements(data, color, bg_color)


    def edit(self, data):
        self.model.update_query(data)


    def form_validation(self, element):
        if '' in [element.email.get().strip(), element.password.get().strip(), element.company.get().strip()]:
            return 'Vous devez remplir tous le formulaire'
        
        check_duplicate_condition = {'email': element.email.get().strip(),\
                                    'password': element.password.get().strip(),\
                                    'url_id': element.url_id,\
                                    'company': element.company.get().strip(),\
                                    }
        
        records = self.model.select_query(columns=['ID'], conditions = check_duplicate_condition)
        # if the record who have the same conf it's not the same
        if len(records) > 1 or (len(records) == 1 and (element.id,) not in records):
            return 'Cette enregistrement il exist déja '

        server_data = self.server_model.select_query(columns=['URL', 'PORT', 'DATABASE'], conditions = {'ID': element.url_id})[0]
        connection_data = {'url':server_data[0]+':'+str(server_data[1]), 'db':server_data[2], 'user':element.email.get().strip(), 'key':element.password.get().strip()}
        print(connection_data)
        if not check_connection(connection_data):
            return 'Les informations de connexion sont fauses'
        return None


    def delete(self, element):
        DeleteConfirmation(element, self.delete_confirmation)
        element.destroy()


    def delete_confirmation(self, element):
        self.model.delete_query(element.id)
        self.user_frame.user_list.frame_list = list(filter(lambda x: x.id != element.id, self.user_frame.user_list.frame_list))
        element.destroy()


    def get_view(self):
        buttons = {'edit': self.show_create_edit_window, 'delete': self.delete}
        user_view = UserView(master=self.view_master, fg_color='white',buttons=buttons)
        user_view.add_button.configure(command=self.show_create_edit_window)
        self.initialize_view(user_view)
        return user_view


    def initialize_view(self, user_view):
        data = self.model.get_data()
        for idx,instance in enumerate(data):
            instance_dict = {'id': instance[0],'email': instance[1],
                            'password':''.join('*' for _ in range(len(instance[2]))),
                            'url_id':instance[3], 'company': instance[4]}

            color, fg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            user_view.user_list.create_elements(instance_dict, color, fg_color)