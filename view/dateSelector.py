# view/date_range_selector.py
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime


class DateRangeSelector(ctk.CTkFrame):
    #Inheritance of customTkinter to visual
    def __init__(self, master, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback #Allow communication with parent

        # Style configuration
        self.font = ctk.CTkFont(family="Arial", size=12)
        self.label_font = ctk.CTkFont(family="Arial", size=12, weight="bold")
        self.configure(fg_color="transparent")  # Para que no destaque el fondo
        self.apply_button.configure(width=100)

        self.create_widgets()

    def create_widgets(self):
        # Configuration to allow visual format
        self.grid_columnconfigure((0, 1, 2, 3), weight=1) #Flex distribution

        # Label of from
        ctk.CTkLabel(self, text="From:", font=self.label_font).grid(
            row=0, column=0, padx=5, pady=5, sticky="e")

        # Selector for "from" with setting visuals for app theme
        self.from_date = DateEntry(
            self,
            font=self.font,
            date_pattern='yyyy-mm-dd',
            background='#2b2b2b',
            foreground='white',
            headersbackground='#2b2b2b',
            selectbackground='#004be0'
        )
        self.from_date.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Label to
        ctk.CTkLabel(self, text="To:", font=self.label_font).grid(
            row=0, column=2, padx=5, pady=5, sticky="e")

        # Selector for "to" with setting visuals for app theme
        self.to_date = DateEntry(
            self,
            font=self.font,
            date_pattern='yyyy-mm-dd',
            background='#2b2b2b',
            foreground='white',
            headersbackground='#2b2b2b',
            selectbackground='#004be0'
        )
        self.to_date.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Ok button
        self.apply_button = ctk.CTkButton(
            self,
            text="Apply",
            command=self.apply_filter
        )
        self.apply_button.grid(row=0, column=4, padx=10, pady=5)

    def apply_filter(self):
        if self.callback:
            try:
                from_date = self.from_date.get_date()
                to_date = self.to_date.get_date()
                if from_date and to_date and from_date > to_date:
                    from_date, to_date = to_date, from_date
                self.callback(from_date, to_date)
            except Exception as e:
                print(f"Error aplicando filtro: {str(e)}")

    def get_dates(self):
        return {
            'from': self.from_date.get_date(),
            'to': self.to_date.get_date()
        }