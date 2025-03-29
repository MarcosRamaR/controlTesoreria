import customtkinter as ctk
from controller.controller import TreasuryController
from functools import partial


class ExpensesView:
    """Class for display the Expenses """

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController() #Controller for data operations

        label = ctk.CTkLabel(self.frame, text="Expenses Control", font=("Arial", 20))
        label.pack(pady=10)

        #Create the header frame for columns
        header_frame = ctk.CTkFrame(self.frame, fg_color=None)
        header_frame.pack(padx=10, pady=10, fill="x")

        #Columns headers
        ctk.CTkLabel(header_frame, text="Invoice Date", width=20, anchor="w").grid(row=0, column=0, padx=5)
        ctk.CTkLabel(header_frame, text="Payment Date", width=20, anchor="w").grid(row=0, column=1, padx=5)
        ctk.CTkLabel(header_frame, text="Company", width=20, anchor="w").grid(row=0, column=2, padx=5)
        ctk.CTkLabel(header_frame, text="Description", width=20, anchor="w").grid(row=0, column=3, padx=5)
        ctk.CTkLabel(header_frame, text="Amount", width=15, anchor="w").grid(row=0, column=4, padx=5)

        #Scrollable frame for the expenses
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame, width=500, height=300)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.selected_row = None
        self.selected_data = None

        self.normal_color = "#2c2f36"  #Default row color
        self.selected_color = "#004be0" #Selected row color

        self.load_expenses()


    def load_expenses(self):
        """Load and display the expenses"""
        print("Loading Data...")
        expenses=self.controller.get_data(type="E")

        #Delete previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        #Create a row for each expense
        for row_index, (_, row) in enumerate(expenses.iterrows()):

            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.normal_color, height=30)
            row_frame.pack(padx=5, pady=2, fill="x")

            #Bind click and hover events
            row_frame.bind("<Button-1>", lambda e, r=row, rf=row_frame: self.on_row_click(r, rf))
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#3e4046"))
            row_frame.bind("<Leave>", lambda e, rf=row_frame: rf.configure(fg_color=self.selected_color if rf == self.selected_row else self.normal_color))

            #Add the data to the row
            ctk.CTkLabel(row_frame, text=row['invoice_date'].strftime('%Y-%m-%d'), anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=row['payment_date'].strftime('%Y-%m-%d'), anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=row['company'], anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=row['description'], anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=f"${row['amount']:.2f}", anchor="w").pack(side="left", padx=5)

    def on_row_click(self, row, row_frame):
        """Handle row selection events"""
        print("Row clicked!")
        # Restore row to normal color
        if self.selected_row:
            self.selected_row.configure(fg_color=self.normal_color)

        #Highlight new selected row
        row_frame.configure(fg_color=self.selected_color)
        self.selected_row = row_frame
        self.selected_data = row

        print(f"Selected data: {row}")

