
import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk
from templates.scrollable_list_frame import ScrollableListFrame
from models.server import ServerModel


class UserView(ctk.CTkFrame):
    def __init__(self, master, buttons=None, **kwargs ):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.user_title = ctk.CTkLabel(master=self, text="Liste des Users", fg_color="white")
        self.user_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.add_button = ctk.CTkButton(master=self, text="Add User")
        self.add_button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.user_list = ScrollableListFrame(master=self,\
                            labels={'email': 200, 'password': 200, 'server_id': 200},\
                            buttons=buttons)
        self.user_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")



class CreateUpdateUser(tk.Tk):

    def __init__(self, server_model=None,  user=None, button= None, create_edit_function= None):
        super().__init__()

        self.title("User")
        self.geometry("360x350")
        self.grid_columnconfigure(0, weight=1)
        self.button = button
        self.user = user
        self.server_model = server_model
        if self.user:
            text = "Edit user"
        else:
            text = 'Create user'

        l2= ctk.CTkLabel(master=self, text=text, font=('Century Gothic',20))
        l2.grid(row=0, column=0,  padx=15, pady=30, sticky="ns")

        self.email=ctk.CTkEntry(master=self, width=220, placeholder_text='email')
        self.email.grid(row=1, column=0,  padx=15, pady=5, sticky="ns")
        
        if self.user:
            self.password=ctk.CTkEntry(master=self, width=220, show="*", placeholder_text='******')
        else:
            self.password=ctk.CTkEntry(master=self, width=220, placeholder_text='password')

        self.password.grid(row=2, column=0,  padx=15, pady=5, sticky="ns")


        self.server_id_names = self.server_model.select_query(columns=['ID','URL'])
        self.server_names = ctk.CTkOptionMenu(self,width=220,fg_color='white',
                                                    text_color="black",
                                                    text_color_disabled="grey",
                                                    button_color="white",
                                                    button_hover_color="white",
                                                    values= list(map(lambda x:x[1], self.server_id_names)),
                                                                command=self.change_server)
        self.server_names.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")
        self.server_names.set(self.server_id_names[0][1])
        #self.server_id=customtkinter.CTkEntry(master=self, width=220, placeholder_text='server_id')
        self.server_id = self.server_id_names[0][0]


        if self.user:
            self.id = self.user.id
            self.email.insert(0,self.user.data_dict.get('email').cget('text'))
            #self.password.insert(0,self.user.data_dict.get('password').cget('text'))
            self.server_names.set(self.user.data_dict.get('server_id').cget('text'))
            pass

        self.validation_text =ctk.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')

        self.button1 = ctk.CTkButton(master=self, width=220, text="Save", command= lambda: self.button_function(create_edit_function), corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")


    def button_function(self, create_edit_function):
        create_edit_function(self)


    def change_server(self,name):
        id = list(filter(lambda x: x[1] == name,self.server_id_names))[0][0]
        self.server_id = id