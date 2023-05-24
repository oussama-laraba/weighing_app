import tkinter as tk
import customtkinter
from models.database_connection import database_connection
from PIL import Image
import os

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.db = database_connection()


        self.company_selection_frame = customtkinter.CTkFrame(master=self, width=200, height=60, fg_color='white')
        
        def company_callback(choice):
            print("company dropdown clicked:", choice)

        self.comany_label = customtkinter.CTkLabel(self.company_selection_frame, text="Company")

        self.comany_label.place( x=10, y=0)

        self.company = customtkinter.CTkOptionMenu(self.company_selection_frame, values=["company 1", "company 2"],
                                                width=150,
                                                command=company_callback)
        self.company.place(x=5, y=30)
        
        self.company_selection_frame.grid(row=0, column=0, padx=15, pady=(5,5))


        self.location_selection_frame = customtkinter.CTkFrame(master=self, width=200, height=60,fg_color='white')

        self.location_label = customtkinter.CTkLabel(self.location_selection_frame, text="Location")

        self.location_label.place( x=10, y=0)

        self.location = customtkinter.CTkOptionMenu(self.location_selection_frame, values=["location 1", "location 2"],
                                                width=150,
                                                command=company_callback)
        self.location.place( x=5, y=30)

        self.location_selection_frame.grid(row=1, column=0, padx=15, pady=(5,5))


        self.product_selection_frame = customtkinter.CTkFrame(master=self, width=200, height=60, fg_color='white')

        self.product_label = customtkinter.CTkLabel(self.product_selection_frame, text="Produit")

        self.product_label.place(x=10 , y=0)

        self.product = customtkinter.CTkOptionMenu(self.product_selection_frame, values=["produit 1", "produit 2"],
                                                width=150,
                                                command=company_callback)
        self.product.place( x=5, y=30)

        self.product_selection_frame.grid(row=2, column=0, padx=15, pady=(5,5))




        self.product_quantity_frame = customtkinter.CTkFrame(master=self, width=200, height=60, fg_color='white')

        self.product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Produit")

        self.product_quantity_label.place(x=10 , y=0)

        self.product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=150)
        self.product_quantity.place( x=5, y=30)


        self.product_quantity_label = customtkinter.CTkLabel(self.product_quantity_frame, text="Produit")

        self.product_quantity_label.place(x=10 , y=0)

        self.product_quantity = customtkinter.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Produit Quantité',
                                                width=150)
        self.product_quantity.place( x=5, y=30)


        self.product_quantity_frame.grid(row=2, column=0, padx=15, pady=(5,5))

        # produit = customtkinter.CTkOptionMenu(self, values=["produit 1", "produit 2"],
        #                                         command=company_callback)
        # produit.grid(row=2, column=0, pady=(10, 10), sticky="we")

        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join('images', "test.jpg")), size=(500, 150))
        self.image_label = customtkinter.CTkLabel(self, text="", image=self.large_test_image)

        self.image_label.grid(row=0, column=1, columnspan=2, rowspan=2, pady=(10, 10), sticky="we")

        def slider_event(value):
            print(value)

        slider = customtkinter.CTkSlider(self, from_=0, to=100, command=slider_event)

        self.server_list = []
