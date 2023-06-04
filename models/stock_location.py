import tkinter as tk
import customtkinter
from models.database_connection import database_connection
from api.stock import get_locations



class StockLocationListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None,  **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.db = database_connection()
        id_odoo = customtkinter.CTkLabel(self, text="id_odoo",  padx=5, width=200, anchor="w")
        location = customtkinter.CTkLabel(self, text='Emplacement', padx=5, width=400,  anchor="w")
        company = customtkinter.CTkLabel(self, text='Entreprise', padx=5, width=200,  anchor="w")

        
        id_odoo.grid(row=0, column=0, pady=(0, 10), sticky="w")
        location.grid(row=0, column=1, pady=(0, 10), sticky="w")
        company.grid(row=0, column=2, pady=(0, 10), sticky="w")
        
        self.command = command

        self.stock_location_list = []

    def add_item(self, instance, color, bg_color):

        stock_location = StockLocation(master=self, instance=instance, color=color, fg_color= bg_color)
        stock_location.grid(row=len(self.stock_location_list)+1, column=0, columnspan=6, pady=(0, 10), sticky="nswe")
        self.stock_location_list.append(stock_location)

    
    def stock_location_initialize(self):
        cursor = self.db.cursor()

        for rec in self.stock_location_list:
            rec.destroy()

        cursor.execute('SELECT * FROM STOCK_LOCATION;')
        for idx,instance in enumerate(cursor.fetchall()):

            color, bg_color = ('green','#e0e0e0') if idx%2 == 1 else ('blue violet', '#C0C0C0')
            self.add_item(instance, color, bg_color)

        cursor.close()
        return None
    

    def refresh_stock_location(self):
        cursor = self.db.cursor()
        records = cursor.execute('DELETE FROM STOCK_LOCATION;')
        # get stock location from odoo api
        stock_location = get_locations(['id','location_id' , 'company_id', 'display_name'])
        # get all stock location ids from sqlite database
        select_locations= 'SELECT ODOO_ID FROM STOCK_LOCATION;'

        cursor.execute(select_locations)
        db_ids = cursor.fetchall()

        # create dictionary have all stock locations ids to make the code
        # run faster even we don't get benefit from it a lot in this case 
        db_ids_dict = {}
        db_ids = list(map(lambda x: db_ids_dict.update({str(x[0]): 1}), db_ids))
        
        # string have all
        stock_location_ids = ''
        for rec in stock_location:
            stock_location_ids += str(rec['id'])+','

            if not db_ids_dict.get(str(rec['id'])):
                create_query = 'INSERT INTO STOCK_LOCATION (ODOO_ID, LOCATION, COMPANY_ID)\
                                VALUES ({},"{}","{}")'.format(rec['id'], rec['display_name'], rec['company_id'][1])
                cursor.execute(create_query)
            


        stock_location_ids = stock_location_ids[:-1]
        delete_query = 'DELETE FROM STOCK_LOCATION\
                        WHERE ODOO_ID NOT IN ('+stock_location_ids+');'

        cursor.execute(delete_query)

        self.db.commit()

        self.stock_location_initialize()
        return None



class StockLocation(customtkinter.CTkFrame):
    def __init__(self, master, instance=None,color=None, stock_location_list=None, **kwargs ):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.db = database_connection()

        self.stock_location_list = stock_location_list

        self.id= instance[0]
        self.id_odoo = customtkinter.CTkLabel(self, text=instance[1], compound="left", padx=5, width=200, anchor="w", text_color=color)
        self.location = customtkinter.CTkLabel(self, text=instance[2], compound="left", padx=5, width=400, anchor="w", text_color=color)
        self.company = customtkinter.CTkLabel(self, text=instance[3], compound="left", padx=5, width=200, anchor="w", text_color=color)

        
        self.id_odoo.grid(row=0, column=0, pady=(5, 5), sticky="w")
        self.location.grid(row=0, column=1, pady=(5, 5), sticky="w")
        self.company.grid(row=0, column=2, pady=(5, 5), sticky="w")
    
        










class StockLocationFrame(customtkinter.CTkFrame):
    def __init__(self, master, db= None, **kwargs ):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.db= database_connection

        self.stock_location_title = customtkinter.CTkLabel(master=self, text="Liste des Emplacement de stock", fg_color="white")
        self.stock_location_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.button = customtkinter.CTkButton(master=self, text="Refresh", command=self.refresh_location_stock)
        self.button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.stock_location_list = StockLocationListFrame(master=self, corner_radius=0, fg_color='#ededed')
        self.stock_location_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
        self.stock_location_list.stock_location_initialize()



    def refresh_location_stock(self):
        self.stock_location_list.refresh_stock_location()





class StockLocationModel():

    def __init__(self):
        self.db = database_connection()

    def get_data(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM STOCK_LOCATION;')
        stock_location = cursor.fetchall()
        cursor.close()
        return stock_location
    
    def select_query(self, columns='*', conditions= None):
        print("perform query select")
        cursor = self.db.cursor()
        query= 'SELECT'
        for column in columns:
            query+= ' '+column+' ,'
        query = query[:-1] + ' FROM STOCK_LOCATION'
        
        if conditions:
            query+= ' WHERE'
            for condition in conditions.items():
                query+= '  '+condition[0].upper()+' = "'+str(condition[1])+'" AND'
            query= query[:-3]
        query+=';'

        print(query)
        data = cursor.execute(query).fetchall()
        cursor.close()
        return data
        

    def create_query(self, data):
        cursor = self.db.cursor()
        create_query = 'INSERT INTO STOCK_LOCATION (ODOO_ID, LOCATION, COMPANY_ID)\
                                VALUES ({},"{}","{}");'.format(data['ODOO_ID'], data['LOCATION'], data['COMPANY_ID'][1])
        id = cursor.execute(create_query).lastrowid
        self.db.commit()
        cursor.close()
        return id

    def update_query(self, data):
        
        print('update query')

    def delete_query(self, ids):
        cursor = self.db.cursor()
        delete_query = 'DELETE FROM STOCK_LOCATION\
                        WHERE ODOO_ID NOT IN ('+ids+');'

        cursor.execute(delete_query)
        self.db.commit()
        cursor.close()
        print('perform delete')