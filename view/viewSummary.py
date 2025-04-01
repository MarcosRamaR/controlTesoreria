import customtkinter as ctk

from controller.controller import TreasuryController


class SummaryView:
    """Class to show graphics"""

    def __init__(self,frame):
        self.frame = frame
        self.controller = TreasuryController()

        self.tabview_summary = ctk.CTkTabview(self.frame)
        self.tabview_summary.pack()

        self.tabview_summary.add("Monthly Balance")
        self.tabview_summary.add("Quaterly Balance")
        self.tabview_summary.add("Yearly Balance")
        self.tabview_summary.add("Treasury Balance")
        self.tabview_summary.add("Expenses")

