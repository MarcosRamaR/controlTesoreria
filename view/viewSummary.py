import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
from controller.controller import TreasuryController
from view.dateSelector import DateRangeSelector



class SummaryView:
    """Class to show graphics"""

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController()
        self.days_period = 30

        #container for tabs
        self.tabview_summary = ctk.CTkTabview(self.frame)
        self.tabview_summary.pack()

        #Create the tabs
        self.tabview_summary.add("Treasury Balance")
        self.tabview_summary.add("Quaterly Balance")
        self.tabview_summary.add("Yearly Balance")
        self.tabview_summary.add("Expenses")

        self.create_treasury_balance_tab()
        self.create_quarter_chart()
        self.create_year_chart()
        self.create_expense_chart()

    def create_treasury_balance_tab(self):
        tab = self.tabview_summary.tab("Treasury Balance")

        #Frame to selectors
        selector_frame = ctk.CTkFrame(tab, fg_color="transparent")
        selector_frame.pack(fill="x", padx=10, pady=5)

        #Date selector
        ctk.CTkLabel(selector_frame, text="Days to show:").pack(side="left", padx=(0, 5))
        self.days_var = ctk.StringVar(value="30")
        days_list = ctk.CTkOptionMenu(
            selector_frame,
            values=["30", "60", "90", "Custom"],
            variable=self.days_var,
            command=self.on_days_change
        )
        days_list.pack(side="left", padx=(0, 10))

        #Range date selector
        self.date_range_selector = DateRangeSelector(
            selector_frame,
            callback=self.update_chart
        )
        self.date_range_selector.pack_forget()

        #Crete the chart
        self.create_days_chart()

    def on_days_change(self,choice):
        if choice == "Custom":
            self.date_range_selector.pack(side="left", fill="x", expand=True)
            self.days_period = 0
        else:
            self.date_range_selector.pack_forget()
            self.days_period = int(choice)
            self.update_chart()
        #Delete previous widgets except days selector
        for widget in self.tabview_summary.tab("Treasury Balance").winfo_children():
            if not (isinstance(widget, ctk.CTkFrame) and not any(isinstance(widget, t) for t in [ctk.CTkLabel, ctk.CTkOptionMenu])):
                widget.destroy()
        #Close matplotlib figures
        plt.close('all')
        self.create_days_chart()

    def update_chart(self, from_date=None, to_date=None):
        #Clear widgets on tabs except days selector
        for tab_name in [ "Treasury Balance", "Quaterly Balance", "Yearly Balance", "Expenses"]:
            for widget in self.tabview_summary.tab(tab_name).winfo_children():
                if not (isinstance(widget, ctk.CTkFrame) and not any(isinstance(widget, t) for t in [ctk.CTkLabel, ctk.CTkOptionMenu])):
                    widget.destroy()

        #To use the range of dates
        if self.days_var.get() == "Custom" and from_date and to_date:
            daily_data = self.controller.get_next_days_balance(
                days = None,  # No usamos days_period en modo custom
                from_date=from_date.strftime('%Y-%m-%d'),
                to_date=to_date.strftime('%Y-%m-%d')
            )
        else:
            daily_data = self.controller.get_next_days_balance(
                self.days_period,
                from_date=from_date.strftime('%Y-%m-%d') if from_date else None,
                to_date=to_date.strftime('%Y-%m-%d') if to_date else None
            )

        self.create_days_chart(daily_data)
        self.create_quarter_chart()
        self.create_year_chart()
        self.create_expense_chart()

    def create_days_chart(self, daily_data=None):
        """Create the graph with selected days range"""
        if daily_data is None:
            daily_data = self.controller.get_next_days_balance(self.days_period)

        #Set the graph
        fig,ax=plt.subplots(figsize=(10,5))

        #Change style
        fig.patch.set_facecolor('#2b2b2b') #"Background" color
        ax.set_facecolor('#2b2b2b') #Inside graph color
        ax.set_title("Treasury Control", color= "white")
        ax.set_xlabel("Date", color= "white")
        ax.set_ylabel("Amounts (€)", color = "white")
        ax.tick_params(colors = "white") #Color to dates and amounts

        #Draw the lines
        if 'I' in daily_data.columns:
            #daily_data.index is the x-axis (dates) daily_data[''] is the y-axis (values)
            ax.plot(daily_data.index,daily_data['I'], color='#228B22',label='Income', marker = 'o', markersize = 5)
        if 'E' in daily_data.columns:
            ax.plot(daily_data.index, daily_data['E'],  color='#d82929', label='Expense', marker='^', markersize = 5)


        max_amount = max(daily_data['I'].max(), daily_data['E'].max())
        plt.yticks(np.arange(0,max_amount+1,100)) #using numpy to range function, and show the Y-axis better

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b')) #Change visual format to dates
        fig.autofmt_xdate()

        ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        ax.grid(True, linestyle="--", alpha=0.3)

        #Add the graph to tkinter on a canvas
        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("Treasury Balance"))
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)


    def create_quarter_chart(self):
        monthly_data=self.controller.get_quarter_balance()

        #Set the graph
        fig,ax = plt.subplots(figsize=(10,5))
        months = monthly_data.index.strftime('%b') #Better format month
        bar_width = 0.3
        x_pos = np.arange(len(months))

        #Draw the bars
        if 'I' in monthly_data.columns:
            #x_pos + bar_width/2 -> Right to central point
            ax.bar(x_pos + bar_width/2, monthly_data['I'],width= bar_width, color='#1c721c',label='Income')
        if 'E' in monthly_data.columns:
            # x_pos + bar_width/2 -> Left to central point
            ax.bar(x_pos - bar_width/2, monthly_data['E'],width= bar_width,  color='#b82525', label='Expense')



        max_amount = max(monthly_data['I'].max(), monthly_data['E'].max())
        plt.yticks(np.arange(0, max_amount + 1, 1000))

        fig.patch.set_facecolor('#2b2b2b') #"Background" color
        ax.set_facecolor('#2b2b2b') #Inside graph color

        #Axis configure
        ax.set_title("Quarterly Balance", pad  =20, color="white")
        ax.set_xlabel("Month", color = "white")
        ax.set_ylabel("Amount (€)", color = "white")
        ax.tick_params(colors="white")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(months)

        ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        ax.grid(axis='y', linestyle="--", alpha=0.3)

        def add_values(bars):
            """Add values to the bars"""
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height,f'€{height:}',ha='center', va='bottom', fontsize=9, color = "white")

        if 'E' in monthly_data.columns:
            add_values(ax.containers[0])
        if 'I' in monthly_data.columns:
            add_values(ax.containers[1 if 'E' in monthly_data.columns else 0])

        plt.tight_layout()

        #Add the graph to tkinter on a canvas
        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("Quaterly Balance"))
        canvas.draw()
        canvas.get_tk_widget().pack()


    def create_year_chart(self):
        monthly_data=self.controller.get_year_balance()

        #Set the graph
        fig,ax = plt.subplots(figsize=(10,5))
        months = monthly_data.index.strftime('%b') #Better format month
        bar_width = 0.3
        x_pos = np.arange(len(months))

        #Draw the bars
        if 'I' in monthly_data.columns:
            #x_pos + bar_width/2 -> Right to central point
            ax.bar(x_pos + bar_width/2, monthly_data['I'],width= bar_width, color='#1c721c',label='Income')
        if 'E' in monthly_data.columns:
            # x_pos + bar_width/2 -> Left to central point
            ax.bar(x_pos - bar_width/2, monthly_data['E'],width= bar_width,  color='#b82525', label='Expense')

        max_amount = max(monthly_data['I'].max(), monthly_data['E'].max())
        plt.yticks(np.arange(0, max_amount + 1, 1000))

        fig.patch.set_facecolor('#2b2b2b') #"Background" color
        ax.set_facecolor('#2b2b2b') #Inside graph color

        #Axis configure
        ax.set_title("Yearly Balance", pad  =20, color="white")
        ax.set_xlabel("Month", color = "white")
        ax.set_ylabel("Amount (€)", color = "white")
        ax.tick_params(colors="white")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(months)

        ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        ax.grid(axis='y', linestyle="--", alpha=0.3)

        def add_values(bars):
            """Add values to the bars"""
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height,f'€{height:}',ha='center', va='bottom', fontsize=9, color = "white")

        if 'E' in monthly_data.columns:
            add_values(ax.containers[0])
        if 'I' in monthly_data.columns:
            add_values(ax.containers[1 if 'E' in monthly_data.columns else 0])

        plt.tight_layout()

        #Add the graph to tkinter on a canvas
        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("Yearly Balance"))
        canvas.draw()
        canvas.get_tk_widget().pack()


    def create_expense_chart(self):
        expenses_company = self.controller.get_data_by_company('E')

        fig, ax = plt.subplots(figsize = (10,5))
        fig.patch.set_facecolor('#2b2b2b')

        #colors = plt.cm.Paired.colors
        colors = [
            '#a51717','#171ca6', '#7ba617','#a65a17','#1aa617','#a68e17','#5ca617','#17a65e','#1787a6','#4417a6','#a617a1',
            '#a1a617',  '#a6175c', '#6f17a6', '#1749a6', '#17a690', '#a67617', '#a63417'
        ]

        #zip() combines two list inot ordered pairs
        labels = [f"{company}(€{amount:,.2f})" for company, amount in zip(expenses_company['company'], expenses_company['amount'])]

        wedges, texts, autotexts = ax.pie(expenses_company['amount'],autopct='%1.1f%%',startangle=90, colors=colors,textprops={'color':'white'},pctdistance=1.1)

        #bbox_to_anchor is to separate the legend
        ax.legend(wedges, labels, facecolor='#2b2b2b', edgecolor='white', labelcolor='white', loc="lower right", bbox_to_anchor=(1.5,0.5))

        ax.set_title('Expenses by Company', color = "white")


        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("Expenses"))
        canvas.draw()
        canvas.get_tk_widget().pack()

    def on_range_mode_change(self, choice):
        """To change visibility of date selector"""
        if choice == "Custom":
            self.date_range_selector.pack(side="left", fill="x", expand=True)
        else:
            self.date_range_selector.pack_forget()
            self.days_period = int(choice)
            self.update_chart()