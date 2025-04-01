import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller.controller import TreasuryController


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


    def create_chart(self):
        daily_data=self.controller.get_next_30days_balance()

        #Set the graph
        fig,ax=plt.subplots(figsize=(10,5))


        #Draw the lines
        if 'I' in daily_data.columns:
            #daily_data.index is the x-axis (dates) daily_data[''] is the y-axis (values)
            ax.plot(daily_data.index,daily_data['I'], 'g-',label='"Income', marker = 'o')
        if 'E' in daily_data.columns:
            ax.plot(daily_data.index, daily_data['E'], 'r-', label='"Expense', marker='^')


        fig.autofmt_xdate()

        ax.legend()
        ax.grid()

        canvas = FigureCanvasTkAgg(fig,master=self.tabview_summary.tab("30 days Balance"))
        canvas.draw()
        canvas.get_tk_widget().pack()