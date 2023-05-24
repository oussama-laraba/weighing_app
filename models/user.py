import tkinter as tk
import customtkinter
from models.database_connection import database_connection

class UserListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, db= None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        self.db = database_connection()
        email = customtkinter.CTkLabel(self, text="Email",  padx=5, anchor="w")
        password = customtkinter.CTkLabel(self, text='Password', padx=5, anchor="w", justify="center")
        url_id_name = customtkinter.CTkLabel(self, text='Url_id', padx=5, anchor="w", justify="center")
        company = customtkinter.CTkLabel(self, text="Company",  padx=5, anchor="w")

        actions = customtkinter.CTkLabel(self, text='Actions', width= 10,padx=5, anchor="w",justify="left")

        
        email.grid(row=0, column=0, pady=(0, 10), sticky="w")
        password.grid(row=0, column=1, pady=(0, 10), sticky="w")
        url_id_name.grid(row=0, column=2, pady=(0, 10), sticky="w")
        company.grid(row=0, column=3, pady=(0, 10), sticky="w")
        actions.grid(row=0, column=4,  columnspan=2,  pady=(0, 10), padx=5,sticky="w")
        
        self.command = command
        self.user_list = []

    def add_item(self, instance, color, bg_color):

        user = User(master=self, instance=instance, color=color, fg_color= bg_color)
        user.grid(row=len(self.user_list)+1, column=0, columnspan=6, pady=(0, 10), sticky="nesw")
        self.user_list.append(user)

    
    def user_initialize(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT U.ID, U.EMAIL, U.PASSWORD, S.URL, U.COMPANY\
                        FROM USER as U\
                        INNER JOIN  SERVER as S ON U.URL_ID = S.ID')
        
        for idx,instance in enumerate(cursor.fetchall()):

            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)


        cursor.close()
        return None
    

class AddUser(customtkinter.CTk):
    
    def __init__(self, edit=False, user=None,user_list=None):
        super().__init__()

        self.title("user")
        self.geometry("360x350")
        self.grid_columnconfigure(0, weight=1)

        self.db = database_connection()
        self.user_list = user_list

        if edit:
            text = "Edit user"
            button_function = lambda: self.edit_user(user)
        else:
            text = 'Create user'
            button_function = self.add_user 

        l2=customtkinter.CTkLabel(master=self, text=text, font=('Century Gothic',20))
        l2.grid(row=0, column=0,  padx=15, pady=30, sticky="ns")

        self.email=customtkinter.CTkEntry(master=self, width=220, placeholder_text='email')
        self.email.grid(row=1, column=0,  padx=15, pady=5, sticky="ns")

        self.password=customtkinter.CTkEntry(master=self, width=220, placeholder_text='password')
        self.password.grid(row=2, column=0,  padx=15, pady=5, sticky="ns")

        cursor = self.db.cursor()
        cursor.execute('SELECT ID, URL FROM SERVER;')

        self.url_id_names = cursor.fetchall()
        self.url_names = customtkinter.CTkOptionMenu(self,width=220,fg_color='white',
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
        #self.url_id.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")

        self.company=customtkinter.CTkEntry(master=self, width=220, placeholder_text='company')
        self.company.grid(row=4, column=0,  padx=15, pady=5, sticky="ns")

        if user:
            self.id = user.id
            self.email.insert(0,user.email.cget('text'))
            self.password.insert(0,user.password.cget('text'))
            self.url_names.set(user.url_id_name.cget('text'))
            self.company.insert(0,user.company.cget('text'))


        self.validation_text =customtkinter.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')
        

        self.button1 = customtkinter.CTkButton(master=self, width=220, text="Save", command=button_function, corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")


    def form_validation(self):
        if '' in [self.email.get().strip(), self.password.get().strip(), self.company.get().strip()]:
            return 'Vous devez remplir tous le formulaire'
        
        
        search_query  = 'SELECT ID FROM USER\
                            WHERE EMAIL = "{}" AND PASSWORD = "{}" AND  URL_ID = {} AND  COMPANY = "{}";'\
                            .format(self.email.get(), self.password.get(), int(self.url_id), self.company.get())
        cursor = self.db.cursor()
        cursor.execute(search_query)
        records = cursor.fetchall()

        # if the record who have the same conf it's not the same
        if len(records) > 1 or (len(records) == 1 and (self.id,) not in records):
            return 'Cette enregistrement il exist déja '
        return None


    def add_user(self):

        validation_text = self.form_validation()
        if not validation_text:
            insert_query  = 'INSERT INTO USER\
                            (EMAIL, PASSWORD, URL_ID, COMPANY)\
                            VALUES ("{}", "{}", {}, "{}");'\
                            .format(self.email.get().strip(),\
                            self.password.get().strip(),\
                            int(self.url_id),\
                            self.company.get().strip())
            
            cursor = self.db.cursor()
            id = cursor.execute(insert_query).lastrowid
            color, bg_color = ('green','#e0e0e0') if len(self.user_list.user_list)%2 == 1 else ('blue violet','#C0C0C0')
            self.user_list.add_item((id,self.email.get(),self.password.get(),self.url_names.get(),self.company.get()), color, bg_color)
            self.db.commit()
            self.destroy()

        else:

            self.button1.grid_forget()
            self.validation_text.configure(text = validation_text)
            self.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            self.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")

    
    def edit_user(self, user):
        validation_text = self.form_validation()
        if not validation_text:
            update_query  = 'UPDATE USER SET\
                            EMAIL = "{}" , PASSWORD = "{}", URL_ID = {}, COMPANY = "{}"\
                            WHERE ID = {};'\
                            .format(self.email.get(), self.password.get(), int(self.url_id), self.company.get(), self.id)
            
            cursor = self.db.cursor()
            cursor.execute(update_query)

            user.email.configure(text = self.email.get())
            user.password.configure(text = self.password.get())
            user.url_id_name.configure(text = self.url_names.get())
            user.company.configure(text = self.company.get())

            self.db.commit()
            self.destroy()

        else:
            self.button1.grid_forget()
            self.validation_text.configure(text = validation_text)
            self.validation_text.grid(row=6, column=0,  padx=15, pady=10, sticky="ns")
            self.button1.grid(row=7, column=0,  padx=15, pady=10, sticky="ns")
    
    def change_url(self,name):
        id = list(filter(lambda x: x[1] == name,self.url_id_names))[0][0]
        self.url_id = id



class User(customtkinter.CTkFrame):
    def __init__(self, master, instance=None,color=None, user_list=None, **kwargs ):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(4, weight=0)
        
        self.db = database_connection()

        self.user_list = user_list

        self.id = instance[0]
        self.email = customtkinter.CTkLabel(self, text=instance[1], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.password = customtkinter.CTkLabel(self, text=instance[2], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.url_id_name = customtkinter.CTkLabel(self, text=instance[3], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.company = customtkinter.CTkLabel(self, text=instance[4], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.edit = customtkinter.CTkButton(self, text="Edit", width=100, height=24, command = self.edit_item)
        self.delete = customtkinter.CTkButton(self, text="Delete", width=100, height=24, command = self.delete_item)

    
        self.email.grid(row=0, column=0, pady=(5, 5), sticky="w")
        self.password.grid(row=0, column=1, pady=(5, 5), sticky="w")
        self.url_id_name.grid(row=0, column=2, pady=(5, 5), sticky="w")
        self.company.grid(row=0, column=3, pady=(5, 5), sticky="w")
        
        self.edit.grid(row=0, column=4, pady=(5, 5), padx=5)
        self.delete.grid(row=0, column=5, pady=(5, 5), padx=5)
        



    def edit_item(self):
        
        edit_user = AddUser(edit=True, user=self)
        edit_user.mainloop()



    def confirm_delete(self):
        self.destroy()

        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM USER WHERE ID = {self.id};")
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





class UserFrame(customtkinter.CTkFrame):
    def __init__(self, master, db= None, **kwargs ):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.db= db

        self.user_title = customtkinter.CTkLabel(master=self, text="Liste des users", fg_color="white")
        self.user_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.button = customtkinter.CTkButton(master=self, text="Add users", command=self.button_add_user)
        self.button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.user_list = UserListFrame(master=self, corner_radius=0, db = self.db, fg_color='#ededed')
        self.user_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
        self.user_list.user_initialize()


    def button_add_user(self):
        add_user = AddUser( user_list=self.user_list )
        add_user.mainloop()

