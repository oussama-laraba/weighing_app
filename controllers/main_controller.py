import sys

# setting path
sys.path.append('../weighing')
import os
from PIL import Image
from models.main import MainModel
import tkinter as tk
import customtkinter as ctk
from views.main_view import MainView
from models.product import  ProductLocationModel
from models.stock_location import StockLocationModel
import helper.bar_code as brc

from helper.weighing import WeighingScaleConnection
import threading
import datetime

class MainController():
    def __init__(self, view_master= None, db= None, api=None,  db_name= None):

        self.db_name= db_name
        #self.model= MainModel()
        self.db = db
        self.api = api
        self.view_master= view_master
        self.stock_location_model = StockLocationModel(db=db)
        self.product_location_model = ProductLocationModel(db=db)
        self.company_values = []
        self.location_values_id = {'NO EMPLACEMENTS':0,}
        self.product_id_values_quantity = []
        self.main_frame = self.get_view()
        self.thread = True
    
    
        
    #reading_thread.start()
    def open_thread(self):
        weighing_connection = WeighingScaleConnection().connection
        if weighing_connection:
            self.reading_thread = threading.Thread(target= self.read_weighing, args=(weighing_connection,))
            self.thread = True
            self.reading_thread.start()

    def close_thread(self):
        self.thread = False

    def read_weighing(self, weighing_connection):
        
        while self.thread:
            weighing_data = weighing_connection.get_data()
            if weighing_data:
                self.change_weighing_data(weighing_data)

    def change_weighing_data(self, data):
        

        self.main_frame.action_frame.product_quantity.configure(state='normal')
        self.main_frame.action_frame.product_quantity.delete(0,tk.END)
        self.main_frame.action_frame.product_quantity.insert(0,data.get('gross'))
        self.main_frame.action_frame.product_quantity.configure(state='disabled')

        self.main_frame.action_frame.confirm_product_quantity.configure(state='normal')
        self.main_frame.action_frame.confirm_product_quantity.delete(0,tk.END)
        self.main_frame.action_frame.confirm_product_quantity.insert(0,data.get('gross'))
        self.main_frame.action_frame.confirm_product_quantity.configure(state='disabled')
        
        self.main_frame.action_frame.product_date.configure(state='normal')
        self.main_frame.action_frame.product_date.delete(0,tk.END)
        self.main_frame.action_frame.product_date.insert(0,datetime.date.today())
        self.main_frame.action_frame.product_date.configure(state='disabled')

        self.main_frame.action_frame.product_time.configure(state='normal')
        self.main_frame.action_frame.product_time.delete(0,tk.END)
        self.main_frame.action_frame.product_time.insert(0,datetime.datetime.now().strftime('%H:%M'))
        self.main_frame.action_frame.product_time.configure(state='disabled')

    def get_view(self):
        # buttons = {'load_companies': self.load_companies,
        #         'load_locations': self.load_locations,
        #         'load_products': self.load_products,
        #         'company_callback': self.company_callback,
        #         'location_callback': self.location_callback,
        #         'product_callback': self.product_callback,
        #         'reset_button': self.reset_button}
        main_view = MainView(master=self.view_master, fg_color='#D2D7D3')
        main_view.action_frame.company.configure(command=self.company_callback)
        main_view.action_frame.location.configure(command=self.location_callback)
        main_view.action_frame.product.configure(command=self.product_callback)
        main_view.action_frame.product_entry.bind('<KeyRelease>', self.product_check_input)
        main_view.action_frame.button_create_bar_code.configure(command=self.create_code_bar_button)
        main_view.show_frame.reset_button.configure(command=self.reset_button)
        self.load_companies(main_view)
        self.load_locations(main_view)
        self.load_products(main_view)
        return main_view
    


    def load_companies(self, main_view):
        cursor = self.db.cursor()
        companies = cursor.execute('SELECT DISTINCT COMPANY_ID FROM STOCK_LOCATION;').fetchall()
        if companies:
            self.company_values = [company[0] for company in companies]
            main_view.action_frame.company.configure(values=self.company_values)
            main_view.action_frame.company.set(companies[0][0])
        cursor.close()


    def load_locations(self, main_view):
        cursor = self.db.cursor()
        id_location = cursor.execute('SELECT ODOO_ID, LOCATION FROM STOCK_LOCATION WHERE COMPANY_ID = "{}";'.format(main_view.action_frame.company.get())).fetchall()
        if id_location:
            self.location_values_id = { location[1]:location[0] for location in id_location }
            locations = list(self.location_values_id.keys())
            main_view.action_frame.location.configure(values=locations)
            main_view.action_frame.location.set(locations[0])
        cursor.close()


    def load_products(self, main_view):

        # cursor = self.db.cursor()
        # products = cursor.execute('SELECT * FROM PRODUCT AS P\
        #                             INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
        #                             INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
        #                             AND  SL.LOCATION = "{}";'.format(self.location.get())).fetchall()
        if main_view.action_frame.location.get() != 'NO EMPLACEMENTS':
            products = self.api.main_product_stock(self.location_values_id[main_view.action_frame.location.get()])
            
            if products:

                self.product_id_values_quantity = [[ product['product_id'][0], product['product_id'][1],\
                                                product['quantity'], product['product_uom_id'][1] ] for product in products]
                #print(self.product_id_values_quantity)
                product_values = [product[1] for product in self.product_id_values_quantity]
                main_view.action_frame.product.configure(values=product_values)
                main_view.action_frame.product.set(self.product_id_values_quantity[0][1])
                color = 'green' if self.product_id_values_quantity[0][2] > 0 else 'red'
                main_view.action_frame.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,} {}'\
                                .format(round(self.product_id_values_quantity[0][2], 2),self.product_id_values_quantity[0][3]).replace(',', ' '), text_color=color)
            else:
                main_view.action_frame.product.configure(values=['NO PRODUCT'])
                main_view.action_frame.product.set('NO PRODUCT')
                main_view.action_frame.product_disponible_quantity_label.configure(text = 'Quantite disponible : 0', text_color='black')
        

    def product_check_input(self, event):
        search = self.main_frame.action_frame.product_entry.get()
        values_quantity = [[product[1], product[2]]  for product in self.product_id_values_quantity]
        copied_values_quantity = list(values_quantity)
        for value in copied_values_quantity:
            if search.lower() not in value[0].lower():
                values_quantity.remove(value)
        
        if values_quantity:
            self.main_frame.action_frame.product.configure(values = [ value[0] for value in values_quantity])
            if len(values_quantity[0][0])> 30:
                self.main_frame.action_frame.product.set(values_quantity[0][0][:30]+' ...')
            else: self.main_frame.action_frame.product.set(values_quantity[0][0])

            color = 'green' if values_quantity[0][1] > 0 else 'red'
            self.main_frame.action_frame.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,} {}'\
                .format(round(values_quantity[0][1], 2), self.product_id_values_quantity[0][3]).replace(',', ' '), text_color=color)

        else:
            self.main_frame.action_frame.product.configure(values = ['NO PRODUCT'])
            self.main_frame.action_frame.product.set('NO PRODUCT')
            self.main_frame.action_frame.product_disponible_quantity_label.configure(text = 'Quantite disponible : 0', text_color='black')
        pass


    def company_callback(self, company):
        self.load_locations(self.main_frame)
        self.load_products(self.main_frame)

    def location_callback(self, location):
        self.load_products(self.main_frame)

    def product_callback(self, product_name):
        if len(product_name)> 30:
            self.main_frame.action_frame.product.set(product_name[:30]+' ...')

        for product in self.product_id_values_quantity:
            if product[1] == product_name:
                color = 'green' if product[2] > 0 else 'red'
                self.main_frame.action_frame.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,} {}'\
                        .format(round(product[2],2), self.product_id_values_quantity[0][3]).replace(',', ' '), text_color=color)


    def create_code_bar_button(self):

        print('create code bar')
        if self.form_validation():
            brc.fill_html_templates(
                self.main_frame.action_frame.product.get(),
                '0000007',
                self.main_frame.action_frame.product_quantity.get(),
                self.main_frame.action_frame.product_disponible_quantity_label.cget('text').split(' ')[-1],
                20,
                self.main_frame.action_frame.extra_info.get('0.0', tk.END)
            )
            brc.gen_display_filled_template_snapshot()
            self.reset_button()
            invoice_image = ctk.CTkImage(Image.open(os.path.join('static/images', "display_filled_template.png")), size=(250, 500))
            self.main_frame.show_frame.invoice_image_label = ctk.CTkLabel(self.main_frame.show_frame, text="", image=invoice_image)
            self.main_frame.show_frame.invoice_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="nswe")
            
        # gen_bar_code(sequence = '12345678910111')     

        # bar_code_img = ctk.CTkImage(Image.open(os.path.join('static/images', "bar_code.png")), size=(200, 150))

        # self.bar_code_image_label.configure( image = bar_code_img)
        # self.bar_code_image_label.image = bar_code_img
        
        # self.invoice_image_label.grid_forget()
        # self.bar_code_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="we")
        # self.button_create_bar_code.grid_forget()
        # self.button_print.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="w")

    def form_validation(self):

        if self.main_frame.action_frame.product.get() == 'NO PRODUCT':
            self.main_frame.action_frame.form_validation_label.configure(text='Veuillez vous choisir le produit s\'il vous plait.', text_color='red')
            self.main_frame.action_frame.form_validation_label.grid(row=5, column=0, sticky="w",  pady=(10,10))
            return False

        if not self.main_frame.action_frame.product_quantity.get():
            self.main_frame.action_frame.form_validation_label.configure(text='Veuillez vous assurer tous les champs sont remplit.', text_color='red')
            self.main_frame.action_frame.form_validation_label.grid(row=5, column=0, sticky="w",  pady=(10,10))
            return False
        
        return True

    def reset_button(self):

        self.main_frame.action_frame.company.set(self.main_frame.action_frame.company.cget("values")[0])
        self.load_locations(self.main_frame)
        self.load_products(self.main_frame)
        
        self.main_frame.action_frame.product_entry.delete(0,tk.END)
        self.main_frame.action_frame.product_entry.configure(placeholder_text= 'BOBINE GALVA - MV')
        
        self.main_frame.action_frame.product_quantity.configure(state='normal')
        self.main_frame.action_frame.product_quantity.delete(0,tk.END)
        self.main_frame.action_frame.product_quantity.configure(placeholder_text= 'Poids')
        self.main_frame.action_frame.product_quantity.configure(state='disabled')

        self.main_frame.action_frame.confirm_product_quantity.configure(state='normal')
        self.main_frame.action_frame.confirm_product_quantity.delete(0,tk.END)
        self.main_frame.action_frame.confirm_product_quantity.configure(placeholder_text= 'Confirm Poids')
        self.main_frame.action_frame.confirm_product_quantity.configure(state='disabled')
        
        self.main_frame.action_frame.product_date.configure(state='normal')
        self.main_frame.action_frame.product_date.delete(0,tk.END)
        self.main_frame.action_frame.product_date.configure(placeholder_text= 'Date')
        self.main_frame.action_frame.product_date.configure(state='disabled')
        
        self.main_frame.action_frame.product_time.configure(state='normal')
        self.main_frame.action_frame.product_time.delete(0,tk.END)
        self.main_frame.action_frame.product_time.configure(placeholder_text= 'Time')
        self.main_frame.action_frame.product_time.configure(state='disabled')
        # self.confirm_product_quantity.configure(text='sfgsfg')

        self.main_frame.action_frame.extra_info.delete('1.0',tk.END)
        self.main_frame.action_frame.form_validation_label.grid_forget()

        if self.main_frame.show_frame.invoice_image_label:
            self.main_frame.show_frame.invoice_image_label.grid_forget()

