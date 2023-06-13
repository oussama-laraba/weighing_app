
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
                            labels={'email': 200, 'password': 200, 'url_id': 200, 'company': 200},\
                            buttons=buttons)
        self.user_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")



class CreateUpdateUser(ctk.CTk):

    def __init__(self, server_model=None,  user=None, button= None, validation_function= None):
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


        self.url_id_names = self.server_model.select_query(columns=['ID','URL'])
        self.url_names = ctk.CTkOptionMenu(self,width=220,fg_color='white',
                                                    text_color="black",
                                                    text_color_disabled="grey",
                                                    button_color="white",
                                                    button_hover_color="white",
                                                    values= list(map(lambda x:x[1], self.url_id_names)),
                                                                command=self.change_url)
        self.url_names.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")
        self.url_names.set(self.url_id_names[0][1])
        #self.url_id=customtkinter.CTkEntry(master=self, width=220, placeholder_text='url_id')
        self.url_id = self.url_id_names[0][0]


        self.company=ctk.CTkEntry(master=self, width=220, placeholder_text='Entreprise')
        self.company.grid(row=4, column=0,  padx=15, pady=5, sticky="ns")

        print(user)

        if self.user:
            self.id = self.user.id
            self.email.insert(0,self.user.data_dict.get('email').cget('text'))
            #self.password.insert(0,self.user.data_dict.get('password').cget('text'))
            self.url_names.set(self.user.data_dict.get('url_id').cget('text'))
            self.company.insert(0,self.user.data_dict.get('company').cget('text'))
            pass

        self.validation_text =ctk.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')
        

        self.button1 = ctk.CTkButton(master=self, width=220, text="Save", command= lambda: self.button_function(validation_function), corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")


    def button_function(self, validation_function):
        validation_text = validation_function(self)
        if not validation_function(self):
            print('valid')
            data = {}
            
            data['ID'] = self.user.id if self.user else None
            data['EMAIL'] = self.email.get().strip()
            data['PASSWORD'] = self.password.get().strip()
            data['URL_ID'] = int(self.url_id)
            data['COMPANY'] = self.company.get().strip()
            self.button(data)

            if self.user:
                self.user.data_dict.get('email').configure(text = self.email.get())
                self.user.data_dict.get('password').configure(text = ''.join('*' for _ in range(len(self.password.get()))))
                self.user.data_dict.get('url_id').configure(text = self.url_names.get())
                self.user.data_dict.get('company').configure(text = self.company.get())

            self.destroy()
        else: 
            self.button1.grid_forget()
            self.validation_text.configure(text = validation_text)
            self.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            self.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")
    

    def change_url(self,name):
        id = list(filter(lambda x: x[1] == name,self.url_id_names))[0][0]
        self.url_id = id