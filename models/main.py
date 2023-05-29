import tkinter as tk
from tkinterhtml import HtmlFrame
from tkhtmlview  import HTMLLabel
from tkPDFViewer import tkPDFViewer as pdf
import customtkinter
from models.database_connection import database_connection
from PIL import Image
from ttkwidgets.autocomplete import AutocompleteCombobox
from api.stock import main_product_stock
import os
from models.bar_code import *
import models.bar_code

class SideBarFrame(customtkinter.CTkFrame):

    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


        self.grid_columnconfigure(0, weight=1)

        self.db = database_connection()


        self.company_selection_frame = customtkinter.CTkFrame(master=self, fg_color='#D2D7D3')
        self.company_selection_frame.grid(row=0, column=0, padx=15, pady=(10,10))
        self.company_selection_frame.grid_columnconfigure(0, weight=1)
        
        self.company_values = []
        self.comany_label = customtkinter.CTkLabel(self.company_selection_frame, text="Company")
        self.comany_label.grid(row=0, column=0, sticky="w")
        self.company = customtkinter.CTkOptionMenu(self.company_selection_frame, values=[],
                                                width=450,
                                                command=self.company_callback)
        self.company.grid(row=1, column=0, sticky="w")



        self.location_selection_frame = customtkinter.CTkFrame(master=self, height=60,fg_color='#D2D7D3')
        self.location_selection_frame.grid(row=1, column=0, padx=15, pady=(10,10))
        self.location_selection_frame.grid_columnconfigure(0, weight=1)
        
        self.location_values_id = {}
        self.location_label = customtkinter.CTkLabel(self.location_selection_frame, text="Location")
        self.location_label.grid(row=0, column=0, sticky="w")
        self.location = customtkinter.CTkOptionMenu(self.location_selection_frame, values=["location 1", "location 2"],
                                                width=450,
                                                command=self.location_callback)
        self.location.grid(row=1, column=0, sticky="w")
        



        
        self.product_selection_frame = customtkinter.CTkFrame(master=self, height=60, width=550, fg_color='#D2D7D3')
        self.product_selection_frame.grid(row=2, column=0, padx=15, pady=(10,10))
        self.product_selection_frame.grid_columnconfigure(0, weight=1)
        self.product_selection_frame.grid_columnconfigure(1, weight=0)

        self.product_id_values_quantity = []
        self.product_label = customtkinter.CTkLabel(self.product_selection_frame, text="Produit")
        self.product_label.grid(row=0, column=0, sticky="w")
        self.product_var = customtkinter.StringVar(value="option 2")
        self.product = customtkinter.CTkOptionMenu(self.product_selection_frame, values=["produit 1", "produit 2"],
                                                width=300,
                                                command=self.product_callback,
                                                variable=self.product_var)
        self.product.grid(row=1, column=0, sticky="w")


        self.product_entry_label = customtkinter.CTkLabel(self.product_selection_frame, text="Chercher Produit")
        self.product_entry_label.grid(row=0, column=1, padx=(15,0), sticky="w")
        self.product_entry = customtkinter.CTkEntry(
                                        self.product_selection_frame, 
                                        )
        self.product_entry.grid(row=1, column=1, padx=(15,0), sticky="w")
        self.product_entry.bind('<KeyRelease>', self.product_check_input)


        self.product_quantity_frame = customtkinter.CTkFrame(master=self,  fg_color='#D2D7D3')
        self.product_quantity_frame.grid(row=3, column=0, padx=15, pady=(10,10))
        self.product_quantity_frame.grid_columnconfigure(0, weight=1)

        self.product_disponible_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="", font=('', 14))
        self.product_disponible_quantity_label.grid(row=0, column=0, sticky="w")

        self.product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Quantite")
        self.product_quantity_label.grid(row=1, column=0, sticky="w")

        self.product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=450)
        self.product_quantity.grid(row=2, column=0, sticky="w",  pady=(0,10))
        self.product_quantity.insert(0,'text')
        self.product_quantity.configure(state='disabled')


        self.confirm_product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Confirme quantite")
        self.confirm_product_quantity_label.grid(row=3, column=0, sticky="w")

        self.confirm_product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=450)
        self.confirm_product_quantity.grid(row=4, column=0, sticky="w")
        self.confirm_product_quantity.insert(0,'text')
        self.confirm_product_quantity.configure(state='disabled')



        self.extra_info_frame = customtkinter.CTkFrame(master=self,  fg_color='#D2D7D3')
        self.extra_info_frame.grid(row=4, column=0, padx=15, pady=(10,10))
        self.extra_info_frame.grid_columnconfigure(0, weight=1)

        self.extra_info_label = customtkinter.CTkLabel(self.extra_info_frame, text="Extra information")
        self.extra_info_label.grid(row=0, column=0, sticky="w")

        self.extra_info = customtkinter.CTkTextbox(self.extra_info_frame,
                                                width=450, height=200)
        self.extra_info.grid(row=1, column=0, sticky="w",  pady=(0,10))

        self.button_create_bar_code= customtkinter.CTkButton(self.extra_info_frame, text="Confirm and create code à bar",
                                                command=self.create_code_bar_button,
                                                width=450)
        self.button_create_bar_code.grid(row=5, column=0, sticky="w",  pady=(10,10))

        self.load_companies()
        self.load_locations()
        self.load_products()



    def load_companies(self):
        cursor = self.db.cursor()
        companies = cursor.execute('SELECT DISTINCT COMPANY_ID FROM STOCK_LOCATION;').fetchall()
        self.company_values = [company[0] for company in companies]
        self.company.configure(values=self.company_values)
        self.company.set(companies[0][0])
        cursor.close()


    def load_locations(self):
        cursor = self.db.cursor()
        id_location = cursor.execute('SELECT ODOO_ID, LOCATION FROM STOCK_LOCATION WHERE COMPANY_ID = "{}";'.format(self.company.get())).fetchall()

        self.location_values_id = { location[1]:location[0] for location in id_location }
        locations = list(self.location_values_id.keys())
        self.location.configure(values=locations)
        self.location.set(locations[0])
        cursor.close()


    def load_products(self):

        # cursor = self.db.cursor()
        # products = cursor.execute('SELECT * FROM PRODUCT AS P\
        #                             INNER JOIN PRODUCT_LOCATION AS PL ON P.ID = PL.PRODUCT_ID\
        #                             INNER JOIN STOCK_LOCATION AS SL ON PL.STOCK_LOCATION_ID = SL.ID\
        #                             AND  SL.LOCATION = "{}";'.format(self.location.get())).fetchall()

        products = main_product_stock(self.location_values_id[self.location.get()])
        self.product_id_values_quantity = [[ product['product_id'][0], product['product_id'][1],\
                                            product['quantity'] ] for product in products]
        if products:
            product_values = [product[1] for product in self.product_id_values_quantity]
            self.product.configure(values=product_values)
            self.product.set(self.product_id_values_quantity[0][1])
            color = 'green' if self.product_id_values_quantity[0][2] > 0 else 'red'
            self.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,}'\
                            .format(round(self.product_id_values_quantity[0][2], 2)).replace(',', ' '), text_color=color)
        else:
            self.product.configure(values=['NO PRODUCT'])
            self.product.set('NO PRODUCT')
            self.product_disponible_quantity_label.configure(text = 'Quantite disponible : 0', text_color='black')

        print(self.product_var.get())
        



    def product_check_input(self, event):
        search = self.product_entry.get()
        values_quantity = [[product[1], product[2]]  for product in self.product_id_values_quantity]
        copied_values_quantity = list(values_quantity)
        for value in copied_values_quantity:
            if search.lower() not in value[0].lower():
                values_quantity.remove(value)
        
        if values_quantity:
            self.product.configure(values = [ value[0] for value in values_quantity])
            if len(values_quantity[0][0])> 30:
                self.product.set(values_quantity[0][0][:30]+' ...')
            else: self.product.set(values_quantity[0][0])

            color = 'green' if values_quantity[0][1] > 0 else 'red'
            self.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,}'\
                .format(round(values_quantity[0][1], 2)).replace(',', ' '), text_color=color)

        else:
            self.product.configure(values = ['NO PRODUCT'])
            self.product.set('NO PRODUCT')
            self.product_disponible_quantity_label.configure(text = 'Quantite disponible : 0', text_color='black')
        pass


    def company_callback(self, company):
        print("company dropdown clicked:", company)
        self.load_locations()
        self.load_products()

    def location_callback(self, location):
        print("location dropdown clicked:", location)
    
        self.load_products()

    def product_callback(self, product_name):
        print("product dropdown clicked:", product_name)
        if len(product_name)> 30:
            self.product.set(product_name[:30]+' ...')

        for product in self.product_id_values_quantity:
            if product[1] == product_name:
                color = 'green' if product[2] > 0 else 'red'
                self.product_disponible_quantity_label.configure(text = 'Quantite disponible : {:,}'\
                        .format(round(product[2],2)).replace(',', ' '), text_color=color)


    def create_code_bar_button(self):
        print('i am now creating the code a bar image and i will show it now')
        
        gen_bar_code(sequence = '12345678910111')      

        bar_code_img = customtkinter.CTkImage(Image.open(os.path.join('static/images', "bar_code.png")), size=(200, 150))

        self.bar_code_image_label.configure( image = bar_code_img)
        self.bar_code_image_label.image = bar_code_img
        
        self.invoice_image_label.grid_forget()
        self.bar_code_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="we")
        self.button_create_bar_code.grid_forget()
        self.button_print.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="w")







class ActionFrame(customtkinter.CTkFrame):

    def __init__(self, master, side_bar = None,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


        self.grid_columnconfigure(0, weight=1)
        self.side_bar = side_bar
        self.product_image = customtkinter.CTkImage(Image.open(os.path.join('static/images', "prod.png")), size=(150, 150))
        self.product_image_label = customtkinter.CTkLabel(self, text="", image=self.product_image)
        self.product_image_label.grid(row=0, column=1, columnspan=2, padx=15, pady=(10,10), sticky="nswe")

        self.invoice_image = customtkinter.CTkImage(Image.open(os.path.join('static/images', "filled_template.png")), size=(250, 500))
        self.invoice_image_label = customtkinter.CTkLabel(self, text="", image=self.invoice_image)
        
        self.invoice_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="nswe")
    


        self.bar_code_image = customtkinter.CTkImage(Image.open(os.path.join('static/images', "bar_code.png")), size=(200, 150))
        self.bar_code_image_label = customtkinter.CTkLabel(self, text="", image=self.bar_code_image)
        


        self.button_reset = customtkinter.CTkButton(self, text="Reset",
                                                command=self.reset_button,
                                                fg_color= "white",
                                                border_color="black",
                                                hover_color= '#D2D7D3',
                                                text_color="black",
                                                border_width=1,
                                                width=100)
        self.button_reset.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="we")


        self.button_print = customtkinter.CTkButton(self, text="Print code à bar",
                                                command=self.print_bar_code,
                                                width=450)
        
        
    
    def print_bar_code(self):
        print('i am now printing the bar code')


    def reset_button(self):
        print('button reset pressed')
        self.side_bar.company.set(self.side_bar.company.cget("values")[0])
        self.side_bar.load_locations()
        self.side_bar.load_products()

        self.side_bar.product_quantity.configure(state='normal')
        self.side_bar.product_quantity.delete(0,tk.END)
        self.side_bar.product_quantity.configure(state='disabled')

        self.side_bar.confirm_product_quantity.configure(state='normal')
        self.side_bar.confirm_product_quantity.delete(0,tk.END)
        self.side_bar.confirm_product_quantity.configure(state='disabled')
        # self.confirm_product_quantity.configure(text='sfgsfg')

        self.side_bar.extra_info.delete('1.0',tk.END)





class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.db = database_connection()


        self.side_bar = SideBarFrame(master=self, fg_color='#D2D7D3', width=700)
        self.side_bar.grid(row=0, column=0, padx=100)


        # produit = customtkinter.CTkOptionMenu(self, values=["produit 1", "produit 2"],
        #                                         command=company_callback)
        # produit.grid(row=2, column=0, pady=(10, 10), sticky="we")

        
        self.action_frame = ActionFrame(master=self,side_bar= self.side_bar, fg_color='#D2D7D3')
        self.action_frame.grid(row=0,column=1, columnspan=2)



