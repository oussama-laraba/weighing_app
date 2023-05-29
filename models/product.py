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

    
    def product_initialize(self, location_id):
        cursor = self.db.cursor()

        for rec in self.product_list:
            rec.destroy()

        cursor.execute('SELECT * FROM PRODUCT AS P\
                        INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
                        INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID AND\
                        SL.ODOO_ID = {};'.format(location_id))
        
        # products = cursor.execute('SELECT * FROM PRODUCT AS P\
        #                             INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
        #                             INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
        #                             AND  SL.LOCATION = "{}";'.format(self.location.get())).fetchall()
        for idx,instance in enumerate(cursor.fetchall()):
            print(instance)
            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)

        cursor.close()
        return None
    

    def refresh_product(self, init_location_id):
        cursor = self.db.cursor()

        # get stock location from odoo api
        products = get_stockable_product()

        # get all stock location ids from sqlite database
        delete_products= 'DELETE FROM PRODUCT;'

        cursor.execute(delete_products)

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


        delete_products= 'DELETE FROM PRODUCT_LOCATION;'

        cursor.execute(delete_products)

        for rec in products:
            product_ids += str(rec['id'])+','

            if not db_ids_dict.get(str(rec['id'])):
                create_query = 'INSERT INTO PRODUCT (ODOO_ID, NAME)\
                                VALUES ({},"{}")'.format(rec['id'], rec['name'])
                
                product_id = cursor.execute(create_query).lastrowid
                if rec.get('location_id'):
                    for location in rec.get('location_id'):
                        location_id = cursor.execute('SELECT ID FROM STOCK_LOCATION WHERE ODOO_ID = {}'.format(location)).fetchone()[0]
                        create_product_location_query = 'INSERT INTO PRODUCT_LOCATION (STOCK_LOCATION_ID, PRODUCT_ID)\
                                                        VALUES ({},{})'.format(location_id, product_id)
                        cursor.execute(create_product_location_query)



        product_ids = product_ids[:-1]
        delete_query = 'DELETE FROM PRODUCT\
                        WHERE ODOO_ID NOT IN ('+product_ids+');'

        cursor.execute(delete_query)

        self.db.commit()


        self.product_initialize(init_location_id)
        return None



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
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.db= database_connection()

        self.product_title = customtkinter.CTkLabel(master=self, text="Liste des Produits stockable", fg_color="white")
        self.product_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.location_values_id = {}
        self.location_label = customtkinter.CTkLabel(master=self, text="Emplacements:", fg_color="white")
        self.location_label.grid(row=0, column=1,  padx=(0,5), pady=5, sticky="e")

        self.location = customtkinter.CTkOptionMenu(self, values=[],
                                                width=250,
                                                command=self.location_callback)
        self.location.grid(row=0, column=2, padx=15, pady=5, sticky="nsew")
        self.load_location()


        self.button = customtkinter.CTkButton(master=self, text="Refresh", command=self.refresh_product)
        self.button.grid(row=0, column=3, padx=15, pady=5, sticky="e")

        self.product_list = ProductListFrame(master=self, corner_radius=0, fg_color='#ededed')
        self.product_list.grid(row=1, column=0, columnspan=4,  padx=15, sticky="nsew")
        
        self.product_list.product_initialize(self.location_values_id[self.location.get()])

    def location_callback(self, name):
        print(f'you have choose the location with the following {self.location_values_id[name]} id ')
        self.product_list.product_initialize(self.location_values_id[name])

    def load_location(self):
        print('you are now loading the locations ')
        cursor = self.db.cursor()
        id_location = cursor.execute('SELECT ODOO_ID, LOCATION FROM STOCK_LOCATION;').fetchall()

        self.location_values_id = { location[1]:location[0] for location in id_location }
        locations = list(self.location_values_id.keys())
        self.location.configure(values=locations)
        self.location.set(locations[0])
        cursor.close()

    def refresh_product(self):
        # products = cursor.execute('SELECT * FROM PRODUCT AS P\
        #                             INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
        #                             INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
        #                             AND  SL.LOCATION = "{}";'.format(self.location.get())).fetchall()
    
        self.location.set(self.location.cget('values')[0])
        self.product_list.refresh_product(self.location_values_id[self.location.get()])