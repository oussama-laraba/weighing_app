import threading

import tkinter as tk
import customtkinter
from models.database_connection import DbConnection
from api.stock import ApiConnection

from models.lot import LotFrame

from controllers.server_controller import SeverController
from controllers.user_controller import UserController
from controllers.stock_location_controller import StockLocationController
from controllers.product_controller import ProductController
from controllers.main_controller import MainController

from helper.weighing import WeighingScaleConnection
from helper.refresh_db import Refresh

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
        self.lot_menu = tk.Menu(self.menubar,  tearoff=0)

        self.main_menu.add_command(
            label="main",
            command= lambda: self.select_main_frame('main'),
            background="white"
        )
        self.main_menu.add_command(
            label="Lots",
            command=lambda: self.select_main_frame('lot'),
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

        self.db = DbConnection().db
        self.api = ApiConnection(db=self.db)
        self.refresher = Refresh(api= self.api, db= self.db)
        # self.main_frame= MainFrame(master=self, fg_color='#D2D7D3')
        # self.main_frame.grid(row=1, column=1, sticky="nsew")
        
        
        
        self.server_frame = None

        

        #self.user_frame = UserFrame(master=self, fg_color='white')
        self.user_frame = None

        self.lot_frame = None


        #self.stock_location_frame = StockLocationFrame(master=self, fg_color='white')
        self.stock_location_frame = None

        #self.stockable_product_frame = ProductFrame(master=self, fg_color='white')
        self.stockable_product_frame = None
        
        self.main_controller = MainController(view_master=self, db=self.db, api=self.api)
        self.main_frame = self.main_controller.main_frame
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.main_controller.open_thread()

        # create scrollable label and button frame
    def close_main_frame(self):
        
        if self.main_frame:
            if self.main_controller:
                self.main_controller.close_thread()
                self.main_controller = None
            self.main_frame.destroy()
        print('close main frame')
        if self.lot_frame:
            self.lot_frame.destroy()

    def select_main_frame(self,name):
        self.close_config_frames()
        self.close_product_frames()
        self.close_stock_frames()

        if name == "main": 
            self.main_controller = MainController(view_master=self, db=self.db, api=self.api)
            self.main_frame = self.main_controller.main_frame
            self.main_frame.grid(row=1, column=1, sticky="nsew")
            self.main_controller.open_thread()
        else:
            if self.main_frame:
                if self.main_controller:
                    self.main_controller.close_thread()
                    self.main_controller = None
                self.main_frame.destroy()

        if name == "lot":
            self.lot_frame = LotFrame(master=self, db=self.db, fg_color='white')
            self.lot_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            if self.lot_frame:
                self.lot_frame.destroy()
    

    def close_config_frames(self):
        if self.server_frame:
            self.server_frame.destroy()
        
        if self.user_frame:
            self.user_frame.destroy()

    def select_config_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_stock_frames()
        self.close_product_frames()

        # show selected frame
        if name == "servers":
            self.server_frame = SeverController(view_master=self, db=self.db ).server_frame
            self.server_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            if self.server_frame:
                self.server_frame.destroy()

        if name == "users":
            self.user_frame = UserController(view_master=self, db=self.db).user_frame
            self.user_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            if self.user_frame:
                self.user_frame.destroy()



    def close_stock_frames(self):
        if self.stock_location_frame:
            self.stock_location_frame.destroy()

    def select_stock_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_config_frames()
        self.close_product_frames()

        # show selected frame
        if name == "location":
            self.stock_location_frame = StockLocationController(view_master = self, db=self.db, api=self.api, refresh_db_function= self.refresher.refresh_location).stock_location_frame
            self.stock_location_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            if self.stock_location_frame:
                self.stock_location_frame.destroy()



    def close_product_frames(self):
        if self.stockable_product_frame:
            self.stockable_product_frame.destroy()

    def select_product_frame_by_name(self, name):
        
        self.close_main_frame()
        self.close_config_frames()
        self.close_stock_frames()
        
        # show selected frame
        if name == "stockable_product":
            self.stockable_product_frame = ProductController(view_master=self, db=self.db, api=self.api, refresh_db_function= self.refresher.refresh_product).product_frame
            self.stockable_product_frame.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        else:
            if self.stockable_product_frame:
                self.stockable_product_frame.destroy()


if __name__ == "__main__":

    app = App2()
    

    def close_app():
        if app.main_controller:
            app.main_controller.close_thread()
        app.destroy()

    app.protocol('WM_DELETE_WINDOW', close_app)

    app.mainloop()
    #app.main_controller.close_thread()





    # reading_thread = threading.Thread(target= read_weighing, args=(10,))
    # reading_thread.start()



        