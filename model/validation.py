from datetime import datetime
import pandas as pd

class Validator:
    @staticmethod
    def validate_date(date):
        """Validate ifs is a valid format to date"""
        try:
            controled_date = datetime.strptime(date,'%Y-%m-%d') #Try parse the date, must be Y nor y for 4 digits year

            if not (pd.Timestamp.min <= pd.Timestamp(controled_date) <= pd.Timestamp.max): #Check if input date have a valid value on Pandas
                return False, f"Date out of range. Must be between {pd.Timestamp.min.date()} and {pd.Timestamp.max.date()}."

            return True,None #If success return true without message
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"

    @staticmethod
    def validate_amount(amount_input):
        """validate if amount is a float"""
        try:
            amount = float(amount_input)
            if amount <= 0:
                return False, "Amount must be more than 0"
            return True,None
        except ValueError:
            return False, "Invalid format for amount. Use numbers"

    @staticmethod
    def validate_data(invoice_date, payment_date, amount):
        """Validate fields"""
        errors={} #Dictionary to save the errors

        valid, message = Validator.validate_date(invoice_date)
        if not valid:
            errors["invoice_date"] = message

        valid, message = Validator.validate_date(payment_date)
        if not valid:
            errors["payment_date"] = message

        valid, message = Validator.validate_amount(amount)
        if not valid:
            errors["amount"] = message

        #if len(errors) == 0 means all valid
        return len(errors) == 0, errors
