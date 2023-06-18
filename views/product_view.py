import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk
from templates.scrollable_list_frame import ScrollableListFrame


class ProductView(ctk.CTkFrame):
    def __init__(self, master, buttons=None, **kwargs ):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)

        self.product_title = ctk.CTkLabel(master=self, text="Liste des Produits stockable", fg_color="white")
        self.product_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.location_values_id = {}
        self.location_label = ctk.CTkLabel(master=self, text="Emplacements:", fg_color="white")
        self.location_label.grid(row=0, column=1,  padx=(0,5), pady=5, sticky="e")

        self.location = ctk.CTkOptionMenu(self, values=[],
                                                width=250,)
        self.location.grid(row=0, column=2, padx=15, pady=5, sticky="nsew")

        self.refresh_button = ctk.CTkButton(master=self, text="Refresher")
        self.refresh_button.grid(row=0, column=3, padx=15, pady=5, sticky="w")

        self.product_list = ScrollableListFrame(master=self,\
                            labels={'id_odoo': 300, 'Produit': 400},\
                            buttons=buttons)
        self.product_list.grid(row=1, column=0, columnspan=4,  padx=15, sticky="nsew")
