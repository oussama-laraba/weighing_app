import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk
from templates.scrollable_list_frame import ScrollableListFrame
from models.stock_location import StockLocationModel

class StockLocationView(ctk.CTkFrame):
    def __init__(self, master, buttons=None, **kwargs ):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.stock_location_title = ctk.CTkLabel(master=self, text="Liste des Emplacement de stock", fg_color="white")
        self.stock_location_title.grid(row=0, column=0,  padx=15, pady=5, sticky="w")

        self.refresh_button = ctk.CTkButton(master=self, text="Refresher")
        self.refresh_button.grid(row=0, column=1, padx=15, pady=5, sticky="ns")

        self.stock_location_list = ScrollableListFrame(master=self,\
                            labels={'id_odoo': 50, 'Emplacement': 400, 'Entreprise': 100},\
                            buttons=buttons)
        self.stock_location_list.grid(row=1, column=0, columnspan=2,  padx=15, sticky="nsew")
