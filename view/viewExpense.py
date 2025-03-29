import customtkinter as ctk
from controller.controller import TreasuryController


class ExpensesView:
    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController()

        label = ctk.CTkLabel(self.frame, text="Expenses Control", font=("Arial", 20))
        label.pack(pady=10)

        self.expense_list = ctk.CTkTextbox(self.frame, height=200)
        self.expense_list.pack(padx=10, pady = 10, fill="both",expand=True)
        self.load_expenses()



    def load_expenses(self):
        print("Cargando gastos...")
        expenses=self.controller.get_data(type="E")
        if expenses.empty:
            print("No expenses found.")
            return
        self.expense_list.delete("1.0","end")
        for _,row in expenses.iterrows():
            self.expense_list.insert("end", f"{row['invoice_date']} - {row['company']} - {row['amount']}\n")






