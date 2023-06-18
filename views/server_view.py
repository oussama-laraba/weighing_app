
import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk
from templates.scrollable_list_frame import ScrollableListFrame


class ServerView(ctk.CTkFrame):
    def __init__(self, master, buttons=None, **kwargs ):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.server_title = ctk.CTkLabel(master=self, text="Liste des Serveurs", fg_color="white")
        self.server_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.add_button = ctk.CTkButton(master=self, text="Add Server")
        self.add_button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.server_list = ScrollableListFrame(master=self,\
                            labels={'url': 100, 'port': 50, 'database': 100, 'key': 400},\
                            buttons=buttons)
        self.server_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")



class CreateUpdateServer(tk.Tk):

    def __init__(self, edit=False, server=None, button= None, create_edit_function= None ,):
        super().__init__()

        print('inside the createupdate init method')
        self.title("Server")
        self.geometry("360x350" )
        self.grid_columnconfigure(0, weight=1)
        self.button = button
        self.edit = edit
        self.server = server
        if self.edit:
            text = "Edit server"
        else:
            text = 'Create server'

        l2= ctk.CTkLabel(master=self, text=text, font=('Century Gothic',20))
        l2.grid(row=0, column=0,  padx=15, pady=30, sticky="ns")

        self.url=ctk.CTkEntry(master=self, width=220, placeholder_text='Url')
        self.url.grid(row=1, column=0,  padx=15, pady=5, sticky="ns")

        self.port=ctk.CTkEntry(master=self, width=220, placeholder_text='Port')
        self.port.grid(row=2, column=0,  padx=15, pady=5, sticky="ns")

        self.database=ctk.CTkEntry(master=self, width=220, placeholder_text='Database')
        self.database.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")

        self.key=ctk.CTkEntry(master=self, width=220, placeholder_text='Key')
        self.key.grid(row=4, column=0,  padx=15, pady=5, sticky="ns")

        if self.server:
            self.id = self.server.id
            self.url.insert(0,self.server.data_dict.get('url').cget('text'))
            self.port.insert(0,self.server.data_dict.get('port').cget('text'))
            self.database.insert(0,self.server.data_dict.get('database').cget('text'))
            self.key.insert(0,self.server.data_dict.get('key').cget('text'))
            pass

        self.validation_text =ctk.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')

        self.button1 = ctk.CTkButton(master=self, width=220, text="Save", command= lambda: self.button_function(create_edit_function), corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")


    def button_function(self, create_edit_function):
        create_edit_function(self)