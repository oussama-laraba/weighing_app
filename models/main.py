import tkinter as tk
import customtkinter
from models.database_connection import database_connection
from PIL import Image
import os

class SideBarFrame(customtkinter.CTkFrame):

    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


        self.grid_columnconfigure(0, weight=1)

        self.db = database_connection()


        self.company_selection_frame = customtkinter.CTkFrame(master=self, fg_color='grey')
        self.company_selection_frame.grid(row=0, column=0, padx=15, pady=(10,10))
        self.company_selection_frame.grid_columnconfigure(0, weight=1)
        


        self.comany_label = customtkinter.CTkLabel(self.company_selection_frame, text="Company")

        self.comany_label.grid(row=0, column=0, sticky="w")

        self.company = customtkinter.CTkOptionMenu(self.company_selection_frame, values=["company 1", "company 2"],
                                                width=350,
                                                command=self.company_callback)
        self.company.grid(row=1, column=0, sticky="w")



        self.location_selection_frame = customtkinter.CTkFrame(master=self, height=60,fg_color='grey')
        self.location_selection_frame.grid(row=1, column=0, padx=15, pady=(10,10))
        self.location_selection_frame.grid_columnconfigure(0, weight=1)
        
        self.location_label = customtkinter.CTkLabel(self.location_selection_frame, text="Location")
        self.location_label.grid(row=0, column=0, sticky="w")

        self.location = customtkinter.CTkOptionMenu(self.location_selection_frame, values=["location 1", "location 2"],
                                                width=350,
                                                command=self.location_callback)
        self.location.grid(row=1, column=0, sticky="w")




        self.product_selection_frame = customtkinter.CTkFrame(master=self, height=60, fg_color='grey')
        self.product_selection_frame.grid(row=2, column=0, padx=15, pady=(10,10))
        self.product_selection_frame.grid_columnconfigure(0, weight=1)

        self.product_label = customtkinter.CTkLabel(self.product_selection_frame, text="Produit")
        self.product_label.grid(row=0, column=0, sticky="w")

        self.product = customtkinter.CTkOptionMenu(self.product_selection_frame, values=["produit 1", "produit 2"],
                                                width=350,
                                                command=self.product_callback)
        self.product.grid(row=1, column=0, sticky="w")



        self.product_quantity_frame = customtkinter.CTkFrame(master=self,  fg_color='grey')
        self.product_quantity_frame.grid(row=3, column=0, padx=15, pady=(10,10))
        self.product_quantity_frame.grid_columnconfigure(0, weight=1)

        self.product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Quantite")
        self.product_quantity_label.grid(row=0, column=0, sticky="w")

        self.product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=350)
        self.product_quantity.grid(row=1, column=0, sticky="w",  pady=(0,10))
        self.product_quantity.insert(0,'text')
        self.product_quantity.configure(state='disabled')


        self.confirm_product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Confirme quantite")
        self.confirm_product_quantity_label.grid(row=2, column=0, sticky="w")

        self.confirm_product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=350)
        self.confirm_product_quantity.grid(row=3, column=0, sticky="w")
        self.confirm_product_quantity.insert(0,'text')
        self.confirm_product_quantity.configure(state='disabled')



        self.extra_info_frame = customtkinter.CTkFrame(master=self,  fg_color='grey')
        self.extra_info_frame.grid(row=4, column=0, padx=15, pady=(10,10))
        self.extra_info_frame.grid_columnconfigure(0, weight=1)

        self.extra_info_label = customtkinter.CTkLabel(self.extra_info_frame, text="Extra information")
        self.extra_info_label.grid(row=0, column=0, sticky="w")

        self.extra_info = customtkinter.CTkTextbox(self.extra_info_frame,
                                                width=350, height=200)
        self.extra_info.grid(row=1, column=0, sticky="w",  pady=(0,10))

        self.button_reset = customtkinter.CTkButton(self.extra_info_frame, text="Reset",
                                                command=self.reset_button,
                                                width=350)
        self.button_reset.grid(row=5, column=0, sticky="w",  pady=(10,10))
        




    def company_callback(self, company):
        print("company dropdown clicked:", company)

    def location_callback(self, location):
        print("location dropdown clicked:", location)

    def product_callback(self, product):
        print("product dropdown clicked:", product)
    

    def reset_button(self):
        print('button reset pressed')
        self.company.set("company 1")
        self.location.set("location 1")
        self.product.set("produit 1")

        self.product_quantity.configure(state='normal')
        self.product_quantity.delete(0,tk.END)
        self.product_quantity.configure(state='disabled')

        self.confirm_product_quantity.configure(state='normal')
        self.confirm_product_quantity.delete(0,tk.END)
        self.confirm_product_quantity.configure(state='disabled')
        # self.confirm_product_quantity.configure(text='sfgsfg')

        self.extra_info.delete('1.0',tk.END)






class ActionFrame(customtkinter.CTkFrame):

    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


        self.grid_columnconfigure(0, weight=1)

        self.product_image = customtkinter.CTkImage(Image.open(os.path.join('images', "test.jpg")), size=(150, 150))
        self.product_image_label = customtkinter.CTkLabel(self, text="", image=self.product_image)
        self.product_image_label.grid(row=0, column=1, columnspan=2, padx=15, pady=(10,10), sticky="nswe")


        self.invoice_image = customtkinter.CTkImage(Image.open(os.path.join('images', "invoice.png")), size=(300, 450))
        self.invoice_image_label = customtkinter.CTkLabel(self, text="", image=self.invoice_image)
        self.invoice_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="nswe")

        self.bar_code_image = customtkinter.CTkImage(Image.open(os.path.join('images', "bar_code.jpg")), size=(200, 150))
        self.bar_code_image_label = customtkinter.CTkLabel(self, text="", image=self.bar_code_image)
        


        self.button_reset = customtkinter.CTkButton(self, text="Confirm and create code à bar",
                                                command=self.create_code_bar_button,
                                                width=350)
        self.button_reset.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="w")


        self.button_print = customtkinter.CTkButton(self, text="Print code à bar",
                                                command=self.print_bar_code,
                                                width=350)
        


    def create_code_bar_button(self):
        print('i am now creating the code a bar image and i will show it now')
        self.invoice_image_label.grid_forget()
        self.bar_code_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="we")
        self.button_reset.grid_forget()
        self.button_print.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="w")

    
    def print_bar_code(self):
        print('i am now printing the bar code')






class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.db = database_connection()


        self.side_bar = SideBarFrame(master=self, fg_color='grey', width=700)
        self.side_bar.grid(row=0, column=0, padx=100)


        # produit = customtkinter.CTkOptionMenu(self, values=["produit 1", "produit 2"],
        #                                         command=company_callback)
        # produit.grid(row=2, column=0, pady=(10, 10), sticky="we")


        self.action_frame = ActionFrame(master=self, fg_color='grey')
        self.action_frame.grid(row=0,column=1, columnspan=2)



