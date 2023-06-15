
import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image




class ActionFrame(ctk.CTkFrame):

    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.company_selection_frame = ctk.CTkFrame(master=self, fg_color='#D2D7D3')
        self.company_selection_frame.grid(row=0, column=0, padx=15, pady=(10,10))
        self.company_selection_frame.grid_columnconfigure(0, weight=1)
        
        self.company_values = []
        self.comany_label = ctk.CTkLabel(self.company_selection_frame, text="Company")
        self.comany_label.grid(row=0, column=0, sticky="w")
        self.company = ctk.CTkOptionMenu(self.company_selection_frame, values=['NO COMPANIES'],
                                                width=450)
        self.company.grid(row=1, column=0, sticky="w")



        self.location_selection_frame = ctk.CTkFrame(master=self, height=60,fg_color='#D2D7D3')
        self.location_selection_frame.grid(row=1, column=0, padx=15, pady=(10,10))
        self.location_selection_frame.grid_columnconfigure(0, weight=1)
        
        self.location_values_id = {}
        self.location_label = ctk.CTkLabel(self.location_selection_frame, text="Location")
        self.location_label.grid(row=0, column=0, sticky="w")
        self.location = ctk.CTkOptionMenu(self.location_selection_frame, values=["NO EMPLACEMENTS"],
                                                width=450,
                                                )
        self.location.grid(row=1, column=0, sticky="w")
        



        
        self.product_selection_frame = ctk.CTkFrame(master=self, height=60, width=550, fg_color='#D2D7D3')
        self.product_selection_frame.grid(row=2, column=0, padx=15, pady=(10,10))
        self.product_selection_frame.grid_columnconfigure(0, weight=1)
        self.product_selection_frame.grid_columnconfigure(1, weight=0)

        self.product_id_values_quantity = []
        self.product_label = ctk.CTkLabel(self.product_selection_frame, text="Produit")
        self.product_label.grid(row=0, column=0, sticky="w")
        self.product_var = ctk.StringVar(value="option 2")
        self.product = ctk.CTkOptionMenu(self.product_selection_frame, values=["NO PRODUCTS"],
                                                width=300,
                                                variable=self.product_var)
        self.product.grid(row=1, column=0, sticky="w")


        self.product_entry_label = ctk.CTkLabel(self.product_selection_frame, text="Chercher Produit")
        self.product_entry_label.grid(row=0, column=1, padx=(15,0), sticky="w")
        self.product_entry = ctk.CTkEntry(self.product_selection_frame, placeholder_text= 'BOBINE GALVA - MV')
        self.product_entry.grid(row=1, column=1, padx=(15,0), sticky="w")


        self.product_quantity_frame = ctk.CTkFrame(master=self,  fg_color='#D2D7D3')
        self.product_quantity_frame.grid(row=3, column=0, padx=15, pady=(10,10))
        self.product_quantity_frame.grid_columnconfigure(0, weight=1)
        self.product_quantity_frame.grid_columnconfigure(1, weight=1)
        self.product_quantity_frame.grid_columnconfigure(2, weight=1)

        self.product_disponible_quantity_label = ctk.CTkLabel(self.product_quantity_frame, text="", font=('', 14))
        self.product_disponible_quantity_label.grid(row=0, column=0, columnspan=2, sticky="w")
        

        self.product_quantity_label = ctk.CTkLabel(self.product_quantity_frame, text="Poids")
        self.product_quantity_label.grid(row=1, column=0, sticky="w")

        self.product_quantity = ctk.CTkEntry(self.product_quantity_frame, placeholder_text= 'Poids', width=150)
        self.product_quantity.grid(row=2, column=0, sticky="w", pady=(0,10))
        self.product_quantity.configure(state='disabled')


        self.product_date_label = ctk.CTkLabel(self.product_quantity_frame, text="Date")
        self.product_date_label.grid(row=1, column=1, padx=(5,5), sticky="w")

        self.product_date = ctk.CTkEntry(self.product_quantity_frame, placeholder_text= 'Date', width=150)
        self.product_date.grid(row=2, column=1, sticky="w", padx=(5,5),  pady=(0,10))
        self.product_date.configure(state='disabled')

        self.product_time_label = ctk.CTkLabel(self.product_quantity_frame, text="Time")
        self.product_time_label.grid(row=1, column=2, sticky="w")

        self.product_time = ctk.CTkEntry(self.product_quantity_frame, placeholder_text= 'Time', width=150)
        self.product_time.grid(row=2, column=2, sticky="w", pady=(0,10))
        self.product_time.configure(state='disabled')

        self.confirm_product_quantity_label = ctk.CTkLabel(self.product_quantity_frame, text="Confirmer Poids")
        self.confirm_product_quantity_label.grid(row=3, column=0, sticky="w")

        self.confirm_product_quantity = ctk.CTkEntry(self.product_quantity_frame,
                                                placeholder_text= 'Confirmer Poids',
                                                width=150)
        self.confirm_product_quantity.grid(row=4, column=0, sticky="w")
        self.confirm_product_quantity.configure(state='disabled')



        self.extra_info_frame = ctk.CTkFrame(master=self,  fg_color='#D2D7D3')
        self.extra_info_frame.grid(row=4, column=0, padx=15, pady=(10,10))
        self.extra_info_frame.grid_columnconfigure(0, weight=1)

        self.extra_info_label = ctk.CTkLabel(self.extra_info_frame, text="Extra information")
        self.extra_info_label.grid(row=0, column=0, sticky="w")

        self.extra_info = ctk.CTkTextbox(self.extra_info_frame,
                                                width=450, height=150)
        self.extra_info.grid(row=1, column=0, sticky="w",  pady=(0,10))
        

        self.button_create_bar_code= ctk.CTkButton(master=self.extra_info_frame, text="Confirm and create code à bar",
                                                width=450)
        self.button_create_bar_code.grid(row=2, column=0, sticky="w",  pady=(10,10))

        self.form_validation_label = ctk.CTkLabel(self.extra_info_frame, text='problem', font=('', 14),width=450)




class ShowFrame(ctk.CTkFrame):

    def __init__(self, master, side_bar = None,  **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


        self.grid_columnconfigure(0, weight=1)
        self.side_bar = side_bar
        self.product_image = ctk.CTkImage(Image.open(os.path.join('static/images', "prod.png")), size=(150, 150))
        self.product_image_label = ctk.CTkLabel(self, text="", image=self.product_image)
        self.product_image_label.grid(row=0, column=1, columnspan=2, padx=15, pady=(10,10), sticky="nswe")

        self.invoice_image = ctk.CTkImage(Image.open(os.path.join('static/images', "display_filled_template.png")), size=(250, 500))
        self.invoice_image_label = ctk.CTkLabel(self, text="", image=self.invoice_image)
        
        self.invoice_image_label.grid(row=1, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="nswe")
    


        self.bar_code_image = ctk.CTkImage(Image.open(os.path.join('static/images', "bar_code.png")), size=(200, 150))
        self.bar_code_image_label = ctk.CTkLabel(self, text="", image=self.bar_code_image)
        


        self.reset_button = ctk.CTkButton(self, text="Reset",
                                                fg_color= "white",
                                                border_color="black",
                                                hover_color= '#D2D7D3',
                                                text_color="black",
                                                border_width=1,
                                                width=100)
        self.reset_button.grid(row=2, column=1, columnspan=2, padx=15, pady=(10,10), sticky="we")

    



class MainView(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


        self.action_frame = ActionFrame(master=self, fg_color='#D2D7D3', width=700)
        self.action_frame.grid(row=0, column=0, padx=100)


        # produit = customtkinter.CTkOptionMenu(self, values=["produit 1", "produit 2"],
        #                                         command=company_callback)
        # produit.grid(row=2, column=0, pady=(10, 10), sticky="we")

        
        self.show_frame = ShowFrame(master=self, fg_color='#D2D7D3')
        self.show_frame.grid(row=0,column=1, columnspan=2)