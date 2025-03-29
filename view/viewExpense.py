import customtkinter as ctk
from controller.controller import TreasuryController
from functools import partial


class ExpensesView:
    """Class for display the Expenses """

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController() #Controller for data operations

        label = ctk.CTkLabel(self.frame, text="Expenses Control", font=("Arial", 20))
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
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.selected_row = None
        self.selected_data = None
        self.normal_color = "#2c2f36"  #Default row color
        self.selected_color = "#004be0" #Selected row color
        self.hover_color = "#3e4046" #Hover color

        self.load_expenses()


    def load_expenses(self):
        """Load and display the expenses"""
        print("Loading Data...")
        expenses=self.controller.get_data(type="E")

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

            #Add the data to the row
            ctk.CTkLabel(row_frame, text=row['invoice_date'].strftime('%Y-%m-%d'), anchor="w").grid(row=0, column=0, padx=5, sticky="w")
            ctk.CTkLabel(row_frame, text=row['payment_date'].strftime('%Y-%m-%d'), anchor="w").grid(row=0, column=1, padx=5, sticky="w")
            ctk.CTkLabel(row_frame, text=row['company'], anchor="w").grid(row=0, column=2, padx=5, sticky="w")
            ctk.CTkLabel(row_frame, text=row['description'], anchor="w",wraplength=300).grid(row=0, column=3, padx=5, sticky="w")
            ctk.CTkLabel(row_frame, text=f"${row['amount']:.2f}", anchor="w").grid(row=0, column=4, padx=5, sticky="w")

            #Bind click and hover events
            row_frame.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=self.hover_color))
            row_frame.bind("<Leave>", lambda e, f=row_frame:f.configure(fg_color=self.selected_color if f == self.selected_row else self.normal_color))
            row_frame.bind("<Button-1>", lambda e, r=row, f=row_frame: self.on_row_click(r, f))


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

