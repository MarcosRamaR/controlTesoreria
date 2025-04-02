import sys

import customtkinter as ctk
from view.viewExpense import ExpensesView
from view.viewIncome import IncomesView
from view.viewSummary import SummaryView

from PIL import Image, ImageTk
import os


class MainInterface:
    def __init__(self, root):
        self.root = root
        self.label = None
        self.summary_view = None
        self.splash_image = None
        self.splash_frame = None
        self.image_label = None
        self.setup_ui()

    def setup_ui(self):
        self.load_icon()
        self.splash_frame = ctk.CTkFrame(self.root, fg_color = None)
        self.splash_frame.pack(fill="both",expand=True)

        try:
            #need this path to can get the image on .exe
            image_path= os.path.join(os.path.dirname(__file__),'..','assets','Logo.png')
            img = Image.open(image_path)

            self.splash_image = ctk.CTkImage(light_image=img,dark_image=img,size=img.size)
            self.image_label = ctk.CTkLabel(self.splash_frame,image=self.splash_image, text="")
            self.image_label.pack()

            self.label = ctk.CTkLabel(self.splash_frame, text="TesControl", font=("Arial", 40))
            self.label.pack(padx=20, pady=20)
        except Exception as e:
            print("No se pudo cargar la imagen")
            self.label = ctk.CTkLabel(self.splash_frame, text="TesControl", font=("Arial", 40))
            self.label.pack(padx=20, pady=20)

        # Change window after 2 secs
        self.root.after(2000, self.change_window)

    def change_window(self):
        # Delete frame
        self.splash_frame.destroy()

        # Creation of tabs
        self.create_tabs()
        self.root.update_idletasks()

    def create_tabs(self):
        # Create a Tabview
        tabview = ctk.CTkTabview(self.root)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Creation 3 tabs
        tabview.add("Summary")
        tabview.add("Expenses")
        tabview.add("Income")

        # Add differente information
        self.summary_view = SummaryView(tabview.tab("Summary"))
        ExpensesView(tabview.tab("Expenses"), self.update_summary) #we need the update function
        IncomesView(tabview.tab("Income"),self.update_summary)

    def update_summary(self):
        if self.summary_view:
            self.summary_view.update_chart()

    def load_icon(self):

        try:
            image_path= "assets/logo.ico"
            self.root.iconbitmap(image_path)
        except Exception as e:
            print("Intentamos logo png")
            try:
                image_path = "assets/Logo.png"
                img = Image.open(image_path)
                photo = ImageTk.PhotoImage(img)
                self.root.wm_iconphoto(True,photo)
            except Exception as e:
                print("Fallo de logo total")
