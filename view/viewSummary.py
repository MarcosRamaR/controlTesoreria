from cProfile import label

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

        self.create_30days_chart()
        self.create_quarter_chart()

    def update_chart(self):
        #Clear widgets on tabs
        for tab_name in ["30 days Balance", "Quaterly Balance", "Yearly Balance", "Treasury Balance", "Expenses"]:
            for widget in self.tabview_summary.tab(tab_name).winfo_children():
                widget.destroy()
        self.create_30days_chart()
        self.create_quarter_chart()

    def create_30days_chart(self):
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
            ax.plot(daily_data.index,daily_data['I'], color='#228B22',label='Income', marker = 'o', markersize = 5)
        if 'E' in daily_data.columns:
            ax.plot(daily_data.index, daily_data['E'],  color='#d82929', label='Expense', marker='^', markersize = 5)

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
            ax.bar(x_pos + bar_width/2, monthly_data['I'],width= bar_width, color='#228B22',label='Income')
        if 'E' in monthly_data.columns:
            # x_pos + bar_width/2 -> Left to central point
            ax.bar(x_pos - bar_width/2, monthly_data['E'],width= bar_width,  color='#d82929', label='Expense')

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
            ax.bar(x_pos + bar_width/2, monthly_data['I'],width= bar_width, color='#228B22',label='Income')
        if 'E' in monthly_data.columns:
            # x_pos + bar_width/2 -> Left to central point
            ax.bar(x_pos - bar_width/2, monthly_data['E'],width= bar_width,  color='#d82929', label='Expense')

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
