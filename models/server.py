import tkinter as tk
import customtkinter
from models.database_connection import database_connection

class ServerListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, db= None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.db = database_connection()
        url = customtkinter.CTkLabel(self, text="Url", anchor="w", width=300 )
        port = customtkinter.CTkLabel(self, text='Port', anchor="w", width=100)
        database = customtkinter.CTkLabel(self, text='Database', anchor="w", width=200)
        key = customtkinter.CTkLabel(self, text="Key", width=400,  anchor="w")

        actions = customtkinter.CTkLabel(self, text='Actions', width= 220, anchor="w")

        
        url.grid(row=0, column=0, pady=(0, 10), sticky="w")
        port.grid(row=0, column=1, pady=(0, 10), sticky="w")
        database.grid(row=0, column=2, pady=(0, 10), sticky="w")
        key.grid(row=0, column=3, pady=(0, 10), sticky="w")
        actions.grid(row=0, column=4,  columnspan=2,  pady=(0, 10), padx=(15, 10),  sticky="w")
        
        self.command = command

        self.server_list = []

    def add_item(self, instance, color, bg_color):

        server = Server(master=self, instance=instance, color=color, fg_color= bg_color)
        server.grid(row=len(self.server_list)+1, column=0, columnspan=6, pady=(0, 10), sticky="nsew")
        self.server_list.append(server)

    
    def server_initialize(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM SERVER;')
        for idx,instance in enumerate(cursor.fetchall()):

            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)

        cursor.close()
        return None
    



class AddServer(customtkinter.CTk):
    
    def __init__(self, edit=False, server=None,server_list=None):
        super().__init__()

        self.title("Server")
        self.geometry("360x350")
        self.grid_columnconfigure(0, weight=1)

        self.db = database_connection()
        self.server_list = server_list

        if edit:
            text = "Edit server"
            button_function = lambda: self.edit_server(server)
        else:
            text = 'Create server'
            button_function = self.add_server 

        l2=customtkinter.CTkLabel(master=self, text=text, font=('Century Gothic',20))
        l2.grid(row=0, column=0,  padx=15, pady=30, sticky="ns")

        self.url=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Url')
        self.url.grid(row=1, column=0,  padx=15, pady=5, sticky="ns")

        self.port=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Port')
        self.port.grid(row=2, column=0,  padx=15, pady=5, sticky="ns")

        self.database=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Database')
        self.database.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")

        self.key=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Key')
        self.key.grid(row=4, column=0,  padx=15, pady=5, sticky="ns")

        if server:
            self.id = server.id
            self.url.insert(0,server.url.cget('text'))
            self.port.insert(0,server.port.cget('text'))
            self.database.insert(0,server.database.cget('text'))
            self.key.insert(0,server.key.cget('text'))

        self.validation_text =customtkinter.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')
        

        self.button1 = customtkinter.CTkButton(master=self, width=220, text="Save", command=button_function, corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")


    def form_validation(self):
        if '' in [self.url.get().strip(), self.port.get().strip(), self.database.get().strip(), self.key.get().strip()]:
            return 'Vous devez remplir tous le formulaire'
        
        if not self.port.get().isnumeric():
            return 'Le port doit etre un entier positive'
        
        search_query  = 'SELECT ID FROM SERVER\
                            WHERE URL = "{}" AND PORT = {} AND  DATABASE = "{}" AND  KEY = "{}";'\
                            .format(self.url.get(), int(self.port.get()), self.database.get(), self.key.get())
        cursor = self.db.cursor()
        cursor.execute(search_query)
        records = cursor.fetchall()

        # if the record who have the same conf it's not the same
        if len(records) > 1 or (len(records) == 1 and (self.id,) not in records):
            return 'Cette enregistrement il exist déja '
        return None


    def add_server(self):

        validation_text = self.form_validation()
        if not validation_text:
            insert_query  = 'INSERT INTO SERVER\
                            (URL, PORT, DATABASE, KEY)\
                            VALUES ("{}", {}, "{}", "{}");'\
                            .format(self.url.get().strip(),\
                            int(self.port.get().strip()),\
                            self.database.get().strip(),\
                            self.key.get().strip())
            
            cursor = self.db.cursor()
            id = cursor.execute(insert_query).lastrowid
            color, bg_color = ('green','#e0e0e0') if len(self.server_list.server_list)%2 == 1 else ('blue violet','#C0C0C0')
            self.server_list.add_item((id,self.url.get(),int(self.port.get()),self.database.get(),self.key.get()), color, bg_color)
            self.db.commit()
            self.destroy()

        else:

            self.button1.grid_forget()
            self.validation_text.configure(text = validation_text)
            self.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            self.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")

    
    def edit_server(self, server):
        validation_text = self.form_validation()
        if not validation_text:
            update_query  = 'UPDATE SERVER SET\
                            URL = "{}" , PORT = {}, DATABASE = "{}", KEY = "{}"\
                            WHERE ID = {};'\
                            .format(self.url.get(), int(self.port.get()), self.database.get(), self.key.get(), self.id)
            
            cursor = self.db.cursor()
            cursor.execute(update_query)
            
            server.url.configure(text = self.url.get())
            server.port.configure(text = self.port.get())
            server.database.configure(text = self.database.get())
            server.key.configure(text = self.key.get())

            self.db.commit()
            self.destroy()

        else:
            self.button1.grid_forget()
            self.validation_text.configure(text = validation_text)
            self.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            self.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")
    pass


class Server(customtkinter.CTkFrame):
    def __init__(self, master, instance=None,color=None, server_list=None, **kwargs ):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(4, weight=0)
        
        self.db = database_connection()

        self.server_list = server_list

        self.id= instance[0]
        self.url = customtkinter.CTkLabel(self, text=instance[1], compound="left", width=300, anchor="w", text_color=color)
        self.port = customtkinter.CTkLabel(self, text=instance[2], compound="left", width=100, anchor="w", text_color=color)
        self.database = customtkinter.CTkLabel(self, text=instance[3], compound="left", width=200, anchor="w", text_color=color)
        self.key = customtkinter.CTkLabel(self, text=instance[4], compound="left", width=400, anchor="w", text_color=color)
        self.edit = customtkinter.CTkButton(self, text="Edit", width=100, height=24, command = self.edit_item)
        self.delete = customtkinter.CTkButton(self, text="Delete", width=100, height=24,  command = self.delete_item)
        
        self.url.grid(row=0, column=0, pady=(5, 5), sticky="w")
        self.port.grid(row=0, column=1, pady=(5, 5), sticky="w")
        self.database.grid(row=0, column=2, pady=(5, 5), sticky="w")
        self.key.grid(row=0, column=3, pady=(5, 5), sticky="w")
        
        self.edit.grid(row=0, column=4, pady=(5, 5), padx=5)
        self.delete.grid(row=0, column=5, pady=(5, 5), padx=5)
        



    def edit_item(self):
        
        edit_server = AddServer(edit=True, server=self)
        edit_server.mainloop()



    def confirm_delete(self):
        self.destroy()

        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM SERVER WHERE ID = {self.id};")
        self.db.commit()
        delete_confirmation.destroy()
        pass

    def cancel_delete(self):
        delete_confirmation.destroy()
        pass


    def delete_item(self):
        
        global delete_confirmation
        delete_confirmation = customtkinter.CTk()
        delete_confirmation.geometry("350x150")
        delete_confirmation.title("CTk example")
        frame = customtkinter.CTkFrame(master=delete_confirmation, width=250, height=150, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5,  anchor=tk.CENTER)

        confirm_text = customtkinter.CTkLabel(master = frame, text='Are you sure you want to delete ??', compound="left", padx=5, anchor="w")
        confirm_button = customtkinter.CTkButton(master=frame, text="ok", command= self.confirm_delete)
        cancel_button = customtkinter.CTkButton(master=frame, text="Cancel", command= self.cancel_delete)

        confirm_text.grid(row=0, columnspan=2,  padx=15, pady=25, sticky="ns")
        confirm_button.grid(row=1, column=0, padx=5, pady=5, sticky="ns")
        cancel_button.grid(row=1, column=1,  padx=5, pady=5, sticky="ns")

        delete_confirmation.mainloop()
        
        return None






class ServerFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs ):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.db= database_connection()

        self.server_title = customtkinter.CTkLabel(master=self, text="Liste des Serveurs", fg_color="white")
        self.server_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.button = customtkinter.CTkButton(master=self, text="Add Server", command=self.button_add_server)
        self.button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.server_list = ServerListFrame(master=self, corner_radius=0, db = self.db, fg_color='#ededed')
        self.server_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
        self.server_list.server_initialize()


    def button_add_server(self):
        add_server = AddServer(server_list=self.server_list)
        add_server.mainloop()

    