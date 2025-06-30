# viewBaseTransaction.py
import customtkinter as ctk
from controller.controller import TreasuryController

class BaseTransactionView:
    """Basic balss to income and expenses views"""

    def __init__(self, frame, transaction_type, title, update_callback=None):
        self.frame = frame
        self.controller = TreasuryController()
        self.update_callback = update_callback
        self.transaction_type = transaction_type  # 'E' or 'I'
        self.title = title

        # Common configuration Ui
        self.setup_ui()

    def setup_ui(self):
        label = ctk.CTkLabel(self.frame, text=f"{self.title} Control", font=("Arial", 20))
        label.pack(pady=(10, 5))

        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=0)

        # Frame to order data
        order_frame = ctk.CTkFrame(container, fg_color=None)
        order_frame.pack(fill="x")

        order_label = ctk.CTkLabel(order_frame, text="Sort by:")
        order_label.pack(side="left", padx=(0, 5))

        self.order_option = ctk.StringVar(value="invoice_date")
        order_options = ["invoice_date", "payment_date", "company", "amount"]
        order_menu = ctk.CTkOptionMenu(order_frame, variable=self.order_option,
                                       values=order_options, command=self.field_order_change)
        order_menu.pack(side="left", padx=(0, 10))

        orientation_label = ctk.CTkLabel(order_frame, text="Order:")
        orientation_label.pack(side="left", padx=(0, 5))

        self.orientation_option = ctk.StringVar(value="descending")
        orientation_menu = ctk.CTkOptionMenu(order_frame, variable=self.orientation_option,
                                             values=['ascending', 'descending'], command=self.orientation_order_change)
        orientation_menu.pack(side="left")

        header_frame = ctk.CTkFrame(container, fg_color=None)
        header_frame.pack(fill="x", pady=(0, 5))

        for i in range(5):
            header_frame.grid_columnconfigure(i, weight=3 if i == 3 else 1, uniform="col")

        headers = ["Invoice Date", "Payment Date", "Company", "Description", "Amount"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, anchor="w").grid(row=0, column=col, padx=5, sticky="ew")

        # Frame with scroll to data
        self.scrollable_frame = ctk.CTkScrollableFrame(container, height=300)
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 5))

        self.selected_row = None
        self.selected_data = None
        self.normal_color = "#2c2f36"
        self.selected_color = "#004be0"
        self.hover_color = "#3e4046"

        self.load_transactions()

        # Detele button
        container_delete_button = ctk.CTkFrame(self.frame, fg_color="transparent", height=1)
        container_delete_button.pack(fill="both", expand=True)

        delete_button = ctk.CTkButton(master=container_delete_button,
                                      text=f"Delete {self.title}",
                                      command=self.button_delete_transaction)
        delete_button.pack(side="right", padx=10)

        # New transaction form
        container_new_transaction = ctk.CTkFrame(self.frame, fg_color="#2c2f36")
        container_new_transaction.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        label_new_transaction = ctk.CTkLabel(container_new_transaction,
                                             text=f"New {self.title}",
                                             font=("Arial", 25))
        label_new_transaction.pack(pady=30)

        frame_new_transaction = ctk.CTkFrame(container_new_transaction, fg_color="transparent")
        frame_new_transaction.pack(fill="both", expand=True)

        # Fields from form
        fields = ["Invoice Date", "Payment Date", "Company", "Description", "Amount"]
        self.entries = {}

        for col, field in enumerate(fields):
            label = ctk.CTkLabel(frame_new_transaction, text=field, font=("Arial", 11))
            label.grid(row=0, column=col, padx=10)

            entry = ctk.CTkEntry(frame_new_transaction)
            entry.grid(row=1, column=col, padx=10, sticky="w")
            self.entries[field.lower().replace(" ", "_")] = entry

        save_button = ctk.CTkButton(master=frame_new_transaction,
                                    text=f"Save {self.title}",
                                    command=self.button_new_transaction)
        save_button.grid(row=1, column=5)

        self.error_frame = ctk.CTkFrame(container_new_transaction, fg_color="transparent", height=20)
        self.error_frame.pack(fill="x")

        self.error_lab = ctk.CTkLabel(self.error_frame, text="", text_color="red", font=("Arial", 10))
        self.error_lab.grid(row=3, column=0, padx=10, pady=(5, 0))

    def button_new_transaction(self):
        print("button new pressed")
        entry_data = {field: entry.get() for field, entry in self.entries.items()}

        self.error_lab.configure(text="")

        success, errors = self.controller.add_new_data(
            entry_data['invoice_date'],
            entry_data['payment_date'],
            entry_data['company'],
            entry_data['description'],
            entry_data['amount'],
            self.transaction_type
        )

        if success:
            for entry in self.entries.values():
                entry.delete(0, 'end')

            self.load_transactions()
            if self.update_callback:
                self.update_callback()
        else:
            error_message = ""
            for field, message in errors.items():
                if field == "invoice_date":
                    error_message += f"Invoice Date: {message}\n"
                elif field == "payment_date":
                    error_message += f"Payment Date: {message}\n"
                elif field == "amount":
                    error_message += f"Amount: {message}\n"

            self.error_lab.configure(text=error_message)

    def button_delete_transaction(self):
        print("button delete pressed")
        if self.selected_row is not None:
            deleted = self.controller.delete_data(
                self.selected_data['invoice_date'],
                self.selected_data['payment_date'],
                self.selected_data['company'],
                self.selected_data['description'],
                self.selected_data['amount'],
                self.transaction_type
            )

            if deleted:
                self.load_transactions()
                self.selected_row = None
                print(f"{self.title} successfully deleted")
                if self.update_callback:
                    self.update_callback()
            else:
                print("Delete error")
        else:
            print(f"No {self.title.lower()} selected")

    def field_order_change(self, field):
        self.load_transactions()

    def orientation_order_change(self, order):
        self.load_transactions()

    def load_transactions(self):
        print("Loading Data...")
        order_by = self.order_option.get()
        ascending = self.orientation_option.get() == "ascending"

        transactions = self.controller.get_data(
            type=self.transaction_type,
            sort_by=order_by,
            ascending=ascending
        )

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for _, row in transactions.iterrows():
            row_container = ctk.CTkFrame(self.scrollable_frame, height=35)
            row_container.pack(fill="x", pady=0)

            row_frame = ctk.CTkFrame(row_container, fg_color=self.normal_color, height=35, corner_radius=0)
            row_frame.pack(fill="both", expand=True)

            for i in range(5):
                row_frame.grid_columnconfigure(i, weight=3 if i == 3 else 1, uniform="col")

            row_frame.bind("<Button-1>", lambda e, r=row, f=row_frame: self.on_row_click(r, f))
            row_frame.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=self.hover_color))
            row_frame.bind("<Leave>", lambda e, f=row_frame: f.configure(
                fg_color=self.selected_color if f == self.selected_row else self.normal_color))

            for col, text in enumerate([
                row['invoice_date'].strftime('%Y-%m-%d'),
                row['payment_date'].strftime('%Y-%m-%d'),
                row['company'],
                row['description'],
                f"€ {row['amount']:.2f}"
            ]):
                label = ctk.CTkLabel(row_frame, text=text, anchor="w", wraplength=300 if col == 3 else 0)
                label.grid(row=0, column=col, padx=5, sticky="w")

                label.bind("<Button-1>", lambda e, r=row, f=row_frame: self.on_row_click(r, f))
                label.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=self.hover_color))
                label.bind("<Leave>", lambda e, f=row_frame: f.configure(
                    fg_color=self.selected_color if f == self.selected_row else self.normal_color))

    def on_row_click(self, row, row_frame):
        print("Row clicked!")
        if self.selected_row:
            self.selected_row.configure(fg_color=self.normal_color)

        row_frame.configure(fg_color=self.selected_color)
        self.selected_row = row_frame
        self.selected_data = row

        print(f"Selected data: {row}")