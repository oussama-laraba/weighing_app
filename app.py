import tkinter as tk
import customtkinter
from models.database_connection import database_connection

from models.server import ServerFrame
from models.user import  UserFrame
from models.stock_location import StockLocationFrame
from models.product import ProductFrame
from models.main import MainFrame

global server_list
global user_list

class App2(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Menu")
        self.geometry("1200x750")
        customtkinter.set_appearance_mode("light")
        self.configure(fg_color='white')


        ## menu
        self.menubar = tk.Menu(self, background='white')
        self.config(menu=self.menubar)

        self.main_menu = tk.Menu(self.menubar, tearoff=0)
        self.product_menu = tk.Menu(self.menubar,  tearoff=0)
        self.stock_menu = tk.Menu(self.menubar,  tearoff=0)
        self.config_menu = tk.Menu(self.menubar,  tearoff=0)


        self.main_menu.add_command(
            label="main",
            command= lambda: self.select_main_frame(),
            background="white"
        )

        self.config_menu.add_command(
            label='Servers',
            command=lambda: self.select_config_frame_by_name('servers'),
            background='white'
        )

        self.config_menu.add_command(
            label='Users',
            command=lambda: self.select_config_frame_by_name('users'),
            background='white'
        )


        self.config_menu.add_command(
            label='Settings',
            command= lambda: self.select_config_frame_by_name('serverframe'),
            background='white'
        )


        self.stock_menu.add_command(
            label='Stock Location',
            command=lambda: self.select_stock_frame_by_name('location'),
            background='white'
        )

        self.stock_menu.add_command(
            label='Stock Quantity',
            command=lambda: self.select_stock_frame_by_name('Stock'),
            background='white'
        )


        self.product_menu.add_command(
            label='Stockable products',
            command=lambda: self.select_product_frame_by_name('stockable_product'),
            background='white'
        )

        self.product_menu.add_command(
            label='Stock Quantity',
            command=lambda: self.select_product_frame_by_name('Stock'),
            background='white'
        )


        self.menubar.add_cascade(
            label="Main",
            menu=self.main_menu
        )

        self.menubar.add_cascade(
            label="Produit",
            menu=self.product_menu
        )

        self.menubar.add_cascade(
            label="Stock",
            menu=self.stock_menu
        )

        self.menubar.add_cascade(
            label="Configuration",
            menu=self.config_menu
        )

        

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.db = database_connection()

        self.main_frame= MainFrame(master=self, fg_color='#D2D7D3')
        self.main_frame.grid(row=1, column=1, sticky="nsew")


        self.server_frame = ServerFrame(master=self, fg_color='white')


        self.user_frame = UserFrame(master=self, fg_color='white')


        self.stock_location_frame = StockLocationFrame(master=self, fg_color='white')


        self.stockable_product_frame = ProductFrame(master=self, fg_color='white')



        
        # create scrollable label and button frame
    def close_main_frame(self):
        self.main_frame.grid_forget()

    def select_main_frame(self):
        self.close_config_frames()
        self.close_product_frames()
        self.close_stock_frames()
        
        self.main_frame.grid(row=1, column=1,sticky="nsew")
    

    def close_config_frames(self):
        self.server_frame.grid_forget()
        self.user_frame.grid_forget()

    def select_config_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_stock_frames()
        self.close_product_frames()

        # show selected frame
        if name == "servers":
            self.server_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            self.server_frame.grid_forget()

        if name == "users":
            self.user_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            self.user_frame.grid_forget()



    def close_stock_frames(self):
        self.stock_location_frame.grid_forget()

    def select_stock_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_config_frames()
        self.close_product_frames()

        # show selected frame
        if name == "location":
            self.stock_location_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            self.stock_location_frame.grid_forget()



    def close_product_frames(self):
        self.stockable_product_frame.grid_forget()

    def select_product_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_config_frames()
        self.close_stock_frames()
        
        # show selected frame
        if name == "stockable_product":
            self.stockable_product_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            self.stockable_product_frame.grid_forget()


if __name__ == "__main__":
    app = App2()
    app.mainloop()