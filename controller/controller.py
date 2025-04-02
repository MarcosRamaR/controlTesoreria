import pandas as pd
from model.model import TreasuryModel
from model.validation import Validator

class TreasuryController:
    def __init__(self):
        self.model = TreasuryModel()
        self.validator = Validator()

    def add_new_data(self,invoice_date,payment_date,company,description,amount,type):
        #Validation of data
        valid, errors = self.validator.validate_data(invoice_date,payment_date,amount)

        if valid:
            self.model.add_treasury_record(invoice_date,payment_date,company,description,amount,type)
            return True,None
        else:
            return False, errors

    def get_data(self, start_date = None, end_date = None, type = None,company = None, sort_by = None, ascending = True):
        return self.model.get_records(start_date,end_date,type,company,sort_by,ascending)

    def get_expenses_summary(self):
        return self.model.get_summary(type = 'E')

    def get_income_summary(self):
        return self.model.get_summary(type = 'I')

    def get_data_by_company(self,type):
        return self.model.get_data_by_company(type)

    def get_monthly_balance(self):
        return self.model.get_monthly_balance()

    def delete_data(self, invoice_date, payment_date,company,description,amount,type):
        return self.model.delete_data(invoice_date, payment_date,company,description,amount,type)

    def get_next_days_balance(self,days=30):
        return self.model.get_next_days(days)

    def get_quarter_balance(self):
        return self.model.get_quarter()

    def get_year_balance(self):
        return self.model.get_year()