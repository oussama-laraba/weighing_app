import sys

# setting path
sys.path.append('../weighing')

import tkinter as tk
import customtkinter as ctk



class ScrollableListFrame(ctk.CTkScrollableFrame):

    def __init__(self, master,  labels= None,  buttons= None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.labels= labels
        self.buttons= buttons
        self.frame_header = self.create_header(self.labels)


    def create_header(self, labels):
        header_frame = ctk.CTkFrame(master = self)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid(row=0, column=0, sticky="nsew")
        labels_dict = {}
        for idx, label in enumerate(labels.items()):
            header_frame.grid_columnconfigure(idx, weight=1)
            lab_obj = ctk.CTkLabel(header_frame, text=label[0], anchor="w", width=label[1])
            lab_obj.grid(row=0, column=idx, pady=(0, 10), sticky="w")
            labels_dict[label[0]] = lab_obj

        if self.buttons:
            actions = ctk.CTkLabel(header_frame, text='Actions', width= 220, anchor="w")
            actions.grid(row=0, column=idx+1,  columnspan=2,  sticky="w")
            labels_dict['actions'] = actions

        return header_frame


    def create_elements(self, data, color, fg_color):
        element_frame = Instance(master = self,data=data, color=color, fg_color= fg_color)
        self.frame_list.append(element_frame)
        return element_frame



class Instance(ctk.CTkFrame):
    def __init__(self, master,   data=None, color=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=len(master.frame_list)+1, column=0, pady=(0, 10), sticky="nsew")
        self.data_dict = {}
        self.id = data['id']

        data.pop('id')
        labels = list(master.labels.values())
        for idx, data in enumerate(list(data.items()), start=0):
            self.grid_columnconfigure(idx, weight=1)
            data_obj = ctk.CTkLabel(self, text=data[1], anchor="w", width=labels[idx], text_color=color)
            data_obj.grid(row=0, column=idx, pady=(5, 5), sticky="w")
            self.data_dict[data[0]] = data_obj

        if master.buttons:
            idx += 1
            if master.buttons.get('edit'):
                button_obj = ctk.CTkButton(self, text='Edit', width=100, height=24, command=lambda: master.buttons['edit'](self))
                button_obj.grid(row=0, column=idx, pady=(5, 5), padx=5)
                self.data_dict['edit'] = button_obj
                idx+=1

            if master.buttons.get('delete'):
                button_obj = ctk.CTkButton(self, text='Delete', width=100, height=24, command=lambda: master.buttons['delete'](self))
                button_obj.grid(row=0, column=idx, pady=(5, 5), padx=5)
                self.data_dict['delete'] = button_obj
                idx+=1

            if master.buttons.get('afficher'):
                button_obj = ctk.CTkButton(self, text='Afficher', width=100, height=24, command=lambda: master.buttons['afficher'](self))
                button_obj.grid(row=0, column=idx, pady=(5, 5), padx=5)
                self.data_dict['afficher'] = button_obj
                idx+=1



class DeleteConfirmation(ctk.CTk):
    def __init__(self, element, confirm_button= None, **kwargs):
        super().__init__(**kwargs)

        self.geometry("350x150")
        self.title("Delete")
        frame = ctk.CTkFrame(master=self, width=250, height=150, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5,  anchor=tk.CENTER)
        self.confirm_button = confirm_button

        confirm_text = ctk.CTkLabel(master = frame, text='Are you sure you want to delete ??', compound="left", padx=5, anchor="w")
        confirm_button = ctk.CTkButton(master=frame, text="ok", command= lambda: self.confirm_delete(element))
        cancel_button = ctk.CTkButton(master=frame, text="Cancel", command= lambda: self.destroy())

        confirm_text.grid(row=0, columnspan=2,  padx=15, pady=25, sticky="ns")
        confirm_button.grid(row=1, column=0, padx=5, pady=5, sticky="ns")
        cancel_button.grid(row=1, column=1,  padx=5, pady=5, sticky="ns")

        self.mainloop()


    def confirm_delete(self,element):
        self.confirm_button(element)
        self.destroy()
