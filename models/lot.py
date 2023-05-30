import tkinter as tk
import customtkinter
from models.database_connection import database_connection

class LotListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, db= None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.db = database_connection()
        lot = customtkinter.CTkLabel(self, text="Lot",  padx=5, anchor="w")
        produit = customtkinter.CTkLabel(self, text='Produit', padx=5, anchor="w", justify="center")
        qty = customtkinter.CTkLabel(self, text='Quantité', padx=5, anchor="w", justify="center")
        location = customtkinter.CTkLabel(self, text="Emplacement",  padx=5, anchor="w")
        barCode = customtkinter.CTkLabel(self, text="Code barré",  padx=5, anchor="w")

        actions = customtkinter.CTkLabel(self, text='Actions', width= 10,padx=5, anchor="center",justify="left")

        
        lot.grid(row=0, column=0, pady=(0, 10), sticky="w")
        produit.grid(row=0, column=1, pady=(0, 10), sticky="w")
        qty.grid(row=0, column=2, pady=(0, 10), sticky="w")
        location.grid(row=0, column=3, pady=(0, 10), sticky="w")
        barCode.grid(row=0, column=4, pady=(0, 10), sticky="w")
        actions.grid(row=0, column=5,  columnspan=2,  pady=(0, 10), padx=5,sticky="w")
        
        self.command = command

        self.lot_list = []

    def add_item(self, instance, color, bg_color):

        lot = Lot(master=self, instance=instance, color=color, fg_color= bg_color)
        lot.grid(row=len(self.lot_list)+1, column=0, columnspan=6, pady=(0, 10), sticky="nesw")
        self.lot_list.append(lot)

    
    def lot_initialize(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM SERVER;')
        for idx,instance in enumerate(cursor.fetchall()):

            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)

        cursor.close()
        return None
    

class EditLot(customtkinter.CTk):
    
    def __init__(self, edit=False, lot=None,lot_list=None):
        super().__init__()

        self.title("Lot")
        self.geometry("360x350")
        self.grid_columnconfigure(0, weight=1)

        self.db = database_connection()
        self.lot_list = lot_list

        if edit:
            text = "Modifier Lot"
            button_function = lambda: self.edit_lot(lot)


        l2=customtkinter.CTkLabel(master=self, text=text, font=('Century Gothic',20))
        l2.grid(row=0, column=0,  padx=15, pady=30, sticky="ns")

        self.lot=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Lot')
        self.lot.grid(row=1, column=0,  padx=15, pady=5, sticky="ns")

        self.produit=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Produit')
        self.produit.grid(row=2, column=0,  padx=15, pady=5, sticky="ns")

        self.qty=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Quantité')
        self.qty.grid(row=3, column=0,  padx=15, pady=5, sticky="ns")

        self.location=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Emplacement')
        self.location.grid(row=4, column=0,  padx=15, pady=5, sticky="ns")

        self.barCode=customtkinter.CTkEntry(master=self, width=220, placeholder_text='Code barré')
        self.barCode.grid(row=5, column=0,  padx=15, pady=5, sticky="ns")

        if lot:
            self.id = lot.id
            self.lot.insert(0,lot.lot.cget('text'))
            self.produit.insert(0,lot.produit.cget('text'))
            self.qty.insert(0,lot.qty.cget('text'))
            self.location.insert(0,lot.qty.cget('text'))
            self.barCode.insert(0,lot.barCode.cget('text'))

        self.validation_text =customtkinter.CTkLabel(master=self, text='', font=('Century Gothic bold',15), text_color='red')
        
        self.button1 = customtkinter.CTkButton(master=self, width=220, text="Sauvgarder", command=button_function, corner_radius=6)
        self.button1.grid(row=6, column=0,  padx=15, pady=30, sticky="ns")

    
    def edit_lot(self, lot):
    
        update_query  = 'UPDATE SERVER SET\
                        URL = "{}" , PORT = {}, DATABASE = "{}", KEY = "{}"\
                        WHERE ID = {};'\
                        .format(self.lot.get(), int(self.produit.get()), self.qty.get(), self.barCode.get(), self.id)
        
        cursor = self.db.cursor()
        cursor.execute(update_query)
        
        lot.lot.configure(text = self.lot.get())
        lot.produit.configure(text = self.produit.get())
        lot.qty.configure(text = self.qty.get())
        lot.location.configure(text = self.location.get())
        lot.barCode.configure(text = self.barCode.get())

        self.db.commit()
        self.destroy()


class Lot(customtkinter.CTkFrame):
    def __init__(self, master, instance=None,color=None, lot_list=None, **kwargs ):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)
        
        
        self.db = database_connection()

        self.lot_list = lot_list

        self.id= instance[0]
        self.lot = customtkinter.CTkLabel(self, text=instance[1], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.produit = customtkinter.CTkLabel(self, text=instance[2], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.qty = customtkinter.CTkLabel(self, text=instance[3], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.barCode = customtkinter.CTkLabel(self, text=instance[4], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.edit = customtkinter.CTkButton(self, text="Modifier", width=100, height=24, command = self.edit_item)
        self.display = customtkinter.CTkButton(self, text="Afficher", width=100, height=24,  command = self.display_item)
        
        self.lot.grid(row=0, column=0, pady=(5, 5), sticky="w")
        self.produit.grid(row=0, column=1, pady=(5, 5), sticky="w")
        self.qty.grid(row=0, column=2, pady=(5, 5), sticky="w")
        self.barCode.grid(row=0, column=3, pady=(5, 5), sticky="w")
        
        self.edit.grid(row=0, column=4, pady=(5, 5), padx=5)
        self.display.grid(row=0, column=5, pady=(5, 5), padx=5)
        

    def edit_item(self):
        
        edit_lot = EditLot(edit=True, lot=self)
        edit_lot.mainloop()

    def display_item(self):
        pass
    

class LotFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs ):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.db= database_connection()

        self.lot_title = customtkinter.CTkLabel(master=self, text="Liste des Lots", fg_color="white")
        self.lot_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.lot_list = LotListFrame(master=self, corner_radius=0, db = self.db, fg_color='#ededed')
        self.lot_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
        self.lot_list.lot_initialize()

