import customtkinter as ctk
from view.viewExpense import ExpensesView
from view.viewIncome import IncomesView


class MainInterface:
    def __init__(self, root):
        self.root = root
        self.label = None
        self.setup_ui()

    def setup_ui(self):
        # Create initial label with app name
        self.label = ctk.CTkLabel(self.root, text="TesControl", font=("Arial", 40))
        self.label.pack(padx=20, pady=20)

        # Change window after 1.5 secs
        self.root.after(1500, self.change_window)

    def change_window(self):
        # Delete first label
        self.label.destroy()

        # Creation of tabs
        self.create_tabs()

    def create_tabs(self):
        # Create a Tabview
        tabview = ctk.CTkTabview(self.root)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Creation 3 tabs
        tabview.add("Summary")
        tabview.add("Expenses")
        tabview.add("Income")

        # Add differente information
        label_p1 = ctk.CTkLabel(tabview.tab("Summary"), text="Summary of the statistics", font=("Arial", 20))
        label_p1.pack(padx=20, pady=20)

        ExpensesView(tabview.tab("Expenses"))
        IncomesView(tabview.tab("Income"))
