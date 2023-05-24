import tkinter as tk
import customtkinter
from models.database_connection import database_connection
from api.stock import get_stockable_product



class ProductListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.db = database_connection()
        id_odoo = customtkinter.CTkLabel(self, text="id_odoo",  padx=5, width=200, anchor="w")
        name = customtkinter.CTkLabel(self, text='name', padx=5, width=400,  anchor="w", justify="center")

        
        id_odoo.grid(row=0, column=0, pady=(0, 10), sticky="w")
        name.grid(row=0, column=1, pady=(0, 10), sticky="w")
        
        self.command = command

        self.product_list = []

    def add_item(self, instance, color, bg_color):

        product = Product(master=self, instance=instance, color=color, fg_color= bg_color)
        product.grid(row=len(self.product_list)+1, column=0, columnspan=6, pady=(0, 10), sticky="nesw")
        self.product_list.append(product)

    
    def product_initialize(self):
        cursor = self.db.cursor()

        for rec in self.product_list:
            rec.destroy()

        cursor.execute('SELECT * FROM PRODUCT;')
        for idx,instance in enumerate(cursor.fetchall()):

            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)

        cursor.close()
        return None
    

    def refresh_product(self):
        cursor = self.db.cursor()

        # get stock location from odoo api
        products = get_stockable_product()

        # get all stock location ids from sqlite database
        select_products= 'SELECT ODOO_ID FROM PRODUCT;'

        cursor.execute(select_products)
        db_ids = cursor.fetchall()

        # create dictionary have all stock locations ids to make the code
        # run faster even we don't get benefit from it a lot in this case 
        db_ids_dict = {}
        db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # string have all
        product_ids = ''
        for rec in products:
            product_ids += str(rec['id'])+','

            if not db_ids_dict.get(str(rec['id'])):
                create_query = 'INSERT INTO PRODUCT (ODOO_ID, NAME)\
                                VALUES ({},"{}")'.format(rec['id'], rec['name'])
                
                print(rec['id'])
                cursor.execute(create_query)
            


        product_ids = product_ids[:-1]
        delete_query = 'DELETE FROM PRODUCT\
                        WHERE ODOO_ID NOT IN ('+product_ids+');'

        cursor.execute(delete_query)

        self.db.commit()

        records = cursor.execute('SELECT * FROM PRODUCT;').fetchall()
        cursor.close()

        self.product_initialize()
        return records



class Product(customtkinter.CTkFrame):
    def __init__(self, master, instance=None,color=None, product_list=None, **kwargs ):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.db = database_connection()

        self.product_list = product_list

        self.id= instance[0]
        self.id_odoo = customtkinter.CTkLabel(self, text=instance[1], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.name = customtkinter.CTkLabel(self, text=instance[2], compound="left", padx=5, width=400, anchor="w", text_color=color)
        
        self.id_odoo.grid(row=0, column=0, pady=(5, 5), sticky="w")
        self.name.grid(row=0, column=1, pady=(5, 5), sticky="w")






class ProductFrame(customtkinter.CTkFrame):
    def __init__(self, master, db= None, **kwargs ):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.db= database_connection

        self.product_title = customtkinter.CTkLabel(master=self, text="Liste des Produits stockable", fg_color="white")
        self.product_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.button = customtkinter.CTkButton(master=self, text="Refresh", command=self.refresh_product)
        self.button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.product_list = ProductListFrame(master=self, corner_radius=0, fg_color='#ededed')
        self.product_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
        self.product_list.product_initialize()



    def refresh_product(self):
        self.product_list.refresh_product()