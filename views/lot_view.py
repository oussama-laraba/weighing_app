
import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk
from templates.scrollable_list_frame import ScrollableListFrame

class LotView(ctk.CTkFrame):
    def __init__(self, master, buttons=None, **kwargs ):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(2, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)

        self.lot_title = ctk.CTkLabel(master=self, text="Liste des Lots", fg_color="white")
        self.lot_title.grid(row=1, column=0,  padx=(15, 25), pady=5, sticky="w")

        self.location_values_id = {}
        self.location_label = ctk.CTkLabel(master=self, text="Emplacements:", fg_color="white")
        self.location_label.grid(row=0, column=1,  padx=(0,5), pady=5, sticky="e")

        self.location = ctk.CTkOptionMenu(self, values=[],
                                                width=250,)
        self.location.grid(row=0, column=2, padx=15, columnspan=2, pady=5, sticky="nsew")

        self.product_values_id = {}
        self.product_label = ctk.CTkLabel(master=self, text="Produits:", fg_color="white")
        self.product_label.grid(row=1, column=1,  padx=(0,5), pady=5, sticky="e")

        self.product = ctk.CTkOptionMenu(self, values=[])
        self.product.grid(row=1, column=2, padx=15, pady=(5,10), sticky="nsew")


        self.product_search = ctk.CTkEntry(self, placeholder_text= 'BOBINE GALVA')
        self.product_search.grid(row=1, column=3, sticky="w", pady=(5,10))

        self.search_button = ctk.CTkButton(master=self, text="Search")
        self.search_button.grid(row=1, column=4, padx=15, pady=5, sticky="w")


        self.refresh_button = ctk.CTkButton(master=self, text="Refresher")
        self.refresh_button.grid(row=0, column=4, padx=15, pady=5, sticky="w")

        self.lot_list = ScrollableListFrame(master=self,\
                            labels={'Lot': 200, 'Produit': 150, 'Quantité': 80, 'Poids': 100, 'Date':100},\
                            buttons=buttons)
        self.lot_list.grid(row=2, column=0, columnspan=5,  padx=15, sticky="nsew")
