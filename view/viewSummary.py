import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from controller.controller import TreasuryController
import numpy as np


class SummaryView:
    """Class to show graphics"""

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController()

        self.tabview_summary = ctk.CTkTabview(self.frame)
        self.tabview_summary.pack()

        self.tabview_summary.add("30 days Balance")
        self.tabview_summary.add("Quaterly Balance")
        self.tabview_summary.add("Yearly Balance")
        self.tabview_summary.add("Treasury Balance")
        self.tabview_summary.add("Expenses")

        self.create_chart()

    def update_chart(self):
        #Clear widgets on tabs
        for tab_name in ["30 days Balance", "Quaterly Balance", "Yearly Balance", "Treasury Balance", "Expenses"]:
            for widget in self.tabview_summary.tab(tab_name).winfo_children():
                widget.destroy()
        self.create_chart()

    def create_chart(self):
        daily_data=self.controller.get_next_30days_balance()

        first_day = daily_data.index[0] #First range day
        last_day = daily_data.index[-1] #Last range day
        days_data = daily_data[daily_data['I'] != 0 | (daily_data['E'] != 0)].index #Days with data
        #Dates we will show (first day, last day and days with data)
        dates_to_show = days_data.union([first_day,last_day]).unique()

        #Set the graph
        fig,ax=plt.subplots(figsize=(10,5))

        #Change style
        fig.patch.set_facecolor('#2b2b2b') #"Background" color
        ax.set_facecolor('#2b2b2b') #Inside graph color
        ax.set_title("30 days Treasury Control", color= "white")
        ax.set_xlabel("Date", color= "white")
        ax.set_ylabel("Amounts (€)", color = "white")
        ax.tick_params(colors = "white") #Color to dates and amounts

        #Draw the lines
        if 'I' in daily_data.columns:
            #daily_data.index is the x-axis (dates) daily_data[''] is the y-axis (values)
            ax.plot(daily_data.index,daily_data['I'], 'g-',label='Income', marker = 'o')
        if 'E' in daily_data.columns:
            ax.plot(daily_data.index, daily_data['E'], 'r-', label='Expense', marker='^')

        max_amount = max(daily_data['I'].max(), daily_data['E'].max())
        plt.yticks(np.arange(0,max_amount+1,500)) #using numpy to range function, and show the Y-axis better

        ax.set_xticks(dates_to_show)
        #ax.set_xticks(daily_data.index) #Forces to show all dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b')) #Change visual format to dates
        fig.autofmt_xdate()

        ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        ax.grid(True, linestyle="--", alpha=0.3)

        #Add the graph to tkinter on a canvas
        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("30 days Balance"))
        canvas.draw()
        canvas.get_tk_widget().pack()