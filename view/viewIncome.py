import customtkinter as ctk
from controller.controller import TreasuryController
from functools import partial


class IncomesView:
    """Class for display the Expenses """

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController() #Controller for data operations

        label = ctk.CTkLabel(self.frame, text="Income Control", font=("Arial", 20))
        label.pack(pady=(10,5))

        #Container for better alignment
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=0)

        #Create the header frame for columns
        header_frame = ctk.CTkFrame(container, fg_color=None)
        header_frame.pack(fill="x", pady=(0, 5))

        for i in range(5):
            header_frame.grid_columnconfigure(i, weight=3 if i == 3 else 1, uniform="col")

        #Column titles
        headers = ["Invoice Date", "Payment Date", "Company", "Description", "Amount"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(header_frame,text=text,anchor="w").grid(row=0, column=col, padx=5, sticky="ew")

        #Scrollable frame for the expenses
        self.scrollable_frame = ctk.CTkScrollableFrame(container, height=300)
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 5))

        self.selected_row = None
        self.selected_data = None
        self.normal_color = "#2c2f36"  #Default row color
        self.selected_color = "#004be0" #Selected row color
        self.hover_color = "#3e4046" #Hover color

        self.load_incomes()

        #Container and button for delete
        container_delete_button = ctk.CTkFrame(self.frame, fg_color="transparent", height=1)
        container_delete_button.pack(fill="both", expand=True)

        delete_income = ctk.CTkButton(master=container_delete_button, text="Delete Expense", command=self.button_delete_income)
        delete_income.pack(side="right", padx=10)

        #Frame to new expense form
        container_new_income = ctk.CTkFrame(self.frame, fg_color="#2c2f36")
        container_new_income.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        label_new_income = ctk.CTkLabel(container_new_income, text="New Expense", font=("Arial", 25))
        label_new_income.pack(pady=30)

        frame_new_income = ctk.CTkFrame(container_new_income,fg_color = "transparent")
        frame_new_income.pack(fill="both", expand=True)

        label_invoice = ctk.CTkLabel(frame_new_income, text = "Invoice Date", font=("Arial", 11))
        label_invoice.grid(row=0, column = 0,padx=10)

        self.entry_invoice = ctk.CTkEntry(frame_new_income)
        self.entry_invoice.grid(row=1, column=0, padx=10, sticky="w")

        label_payment = ctk.CTkLabel(frame_new_income, text = "Payment Date", font=("Arial", 11))
        label_payment.grid(row=0, column = 1,padx=10)

        self.entry_payment = ctk.CTkEntry(frame_new_income)
        self.entry_payment.grid(row=1, column=1, padx=10, sticky="w")

        label_company = ctk.CTkLabel(frame_new_income, text = "Company", font=("Arial", 11))
        label_company .grid(row=0, column = 2,padx=10)

        self.entry_company  = ctk.CTkEntry(frame_new_income)
        self.entry_company .grid(row=1, column=2, padx=10, sticky="w")

        label_descr = ctk.CTkLabel(frame_new_income, text = "Description", font=("Arial", 11))
        label_descr.grid(row=0, column = 3,padx=10)

        self.entry_descr = ctk.CTkEntry(frame_new_income)
        self.entry_descr.grid(row=1, column=3, padx=10, sticky="w")

        label_amount = ctk.CTkLabel(frame_new_income, text = "Amount", font=("Arial", 11))
        label_amount.grid(row=0, column = 4,padx=10)

        self.entry_amount = ctk.CTkEntry(frame_new_income)
        self.entry_amount.grid(row=1, column=4, padx=10, sticky="w")

        save_income = ctk.CTkButton(master=frame_new_income, text="Save Expense", command=self.button_new_income)
        save_income.grid(row=1, column=5)


    def button_new_income(self):
        print("button new pressed")
        entry_invoice= self.entry_invoice.get()
        entry_payment = self.entry_payment.get()
        entry_company= self.entry_company.get()
        entry_descr = self.entry_descr.get()
        entry_amount =self.entry_amount.get()

        self.controller.add_new_data(entry_invoice,entry_payment,entry_company,entry_descr,entry_amount,"I")
        self.load_incomes()

    def button_delete_income(self):
        print("button delete pressed")
        if self.selected_row is not None:
            invoice_date = self.selected_data['invoice_date']
            payment_date = self.selected_data['payment_date']
            company = self.selected_data['company']
            description = self.selected_data['description']
            amount = self.selected_data['amount']

            deleted = self.controller.delete_data(invoice_date,payment_date,company,description,amount,'I')

            if deleted:
                self.load_incomes()
                self.selected_row = None
                print("Income successfully deleted")
            else:
                print("Deleted error")
        else:
            print("No expense selected")



    def load_incomes(self):
        """Load and display the expenses"""
        print("Loading Data...")
        expenses=self.controller.get_data(type="I")

        #Delete previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        #Create a row for each expense
        for _, row in expenses.iterrows():

            # Create row container
            row_container = ctk.CTkFrame(self.scrollable_frame, height=35)
            row_container.pack(fill="x", pady=0)

            #Row frame to better events
            row_frame = ctk.CTkFrame(row_container, fg_color=self.normal_color, height=35,corner_radius=0)
            row_frame.pack(fill="both", expand=True)

            #To respect same weights as headers
            for i in range(5):
                row_frame.grid_columnconfigure(i, weight=3 if i == 3 else 1, uniform="col")

            # Bind click event to the entire row_frame
            row_frame.bind("<Button-1>", lambda e, r=row, f=row_frame: self.on_row_click(r, f))
            row_frame.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=self.hover_color))
            row_frame.bind("<Leave>", lambda e, f=row_frame: f.configure(fg_color=self.selected_color if f == self.selected_row else self.normal_color))

            # Add the data to the row
            for col, text in enumerate([
                row['invoice_date'].strftime('%Y-%m-%d'),
                row['payment_date'].strftime('%Y-%m-%d'),
                row['company'],
                row['description'],
                f"€ {row['amount']:.2f}"
            ]):
                label = ctk.CTkLabel(row_frame, text=text, anchor="w", wraplength=300 if col == 3 else 0)
                label.grid(row=0, column=col, padx=5, sticky="w")

                # Bind click event to each label to ensure clicks on text are registered
                label.bind("<Button-1>", lambda e, r=row, f=row_frame: self.on_row_click(r, f))
                label.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=self.hover_color))
                label.bind("<Leave>", lambda e, f=row_frame:f.configure(fg_color=self.selected_color if f == self.selected_row else self.normal_color))


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

