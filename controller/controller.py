import pandas as pd
from model.model import TreasuryModel

class TreasuryController:
    def __init__(self):
        self.model = TreasuryModel()

    def add_new_data(self,invoice_date,payment_date,company,description,amount,type):
        self.model.add_new_data(invoice_date,payment_date,company,description,amount,type)

    def get_data(self, start_date = None, end_date = None, type = None,company = None, sort_by = None, ascending = True):
        return self.model.get_records(start_date,end_date,type,company,sort_by,ascending)

    def get_expenses_summary(self):
        return self.model.get_summary(type = 'E')

    def get_income_summary(self):
        return self.model.get_summary(type = 'I')

    def get_expenses_by_company(self):
        return self.model.get_expenses_by_company()

    def get_income_by_company(self):
        return self.model.get_income_by_company()

    def get_monthly_balance(self):
        return self.model.get_monthly_balance()