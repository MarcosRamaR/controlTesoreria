from tkinter.constants import FALSE

import pandas as pd
import os
from datetime import datetime, timedelta


class TreasuryModel:
    def __init__(self, treasury_file = 'treasury_record.csv'):
        self.treasury_file = treasury_file
        self.initialize_file()

    #If not exists file .csv, create
    def initialize_file(self):
        if not os.path.exists(self.treasury_file) or os.stat(self.treasury_file).st_size == 0:
            treasury_columns = [
                'invoice_date',
                'payment_date',
                'company',
                'description',
                'amount',
                'type'
            ]
            pd.DataFrame(columns=treasury_columns).to_csv(self.treasury_file, index = False)

    #Add a new Expense or Income
    def add_treasury_record(self,invoice_date,payment_date,company,description,amount,type):
        # read the file csv and convert it to DataFrame
        df =pd.read_csv(self.treasury_file)

        new_data = pd.DataFrame({
            'invoice_date': [invoice_date],
            'payment_date': [payment_date],
            'company': [company],
            'description': [description],
            'amount': [float(amount)],
            'type': [type]
        })
        if not new_data.empty:
            df = pd.concat([df,new_data], ignore_index = True)
        df.to_csv(self.treasury_file, index = False)

    def get_records(self, start_date = None, end_date = None, type = None,company = None, sort_by = None, ascending = True):
        """
        Get the records with some options
        :param start_date: Start payment date of filter
        :param end_date: End payment date of filter
        :param type: E for expenses, I for incomes
        :param company:
        :param sort_by:
        :param ascengin:
        :return:
        """

        #Transform dates to datatime
        df = pd.read_csv(self.treasury_file)
        df['invoice_date'] = pd.to_datetime(df['invoice_date'])
        df['payment_date'] = pd.to_datetime(df['payment_date'])

        #Filter payment date data between two dates
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            df = df[(df['payment_date'] >= start_date) & (df['payment_date'] <= end_date)]

        #Filter for data type (expense or income)
        if type:
            df = df[df['type'] == type]

        #Filter for company
        if company:
            df = df[df['company'].str.contains(company, case = False)]

        if sort_by:
            try:
                sort_by = sort_by.strip().lower() #Delete spaces and put all on lower case
                if sort_by in df.columns:
                    df = df.sort_values(by=sort_by, ascending= ascending)
                else:
                    print(f"Warning: Column '{sort_by}' not found for sorting. Data will remain unsorted.")
            except Exception as e:
                print(f"Error sorting by {sort_by}: {str(e)}" )

        return df

    def get_summary(self,type = None):
        df = pd.read_csv(self.treasury_file)

        if type:
            df = df[df['type'] == type]

        total = df['amount'].sum()
        avg = df['amount'].mean() if len(df) > 0 else 0

        return total, avg

    def get_data_by_company(self,type):
        df = self.get_records(type=type)
        return df.groupby('company')['amount'].sum().reset_index()

    def get_monthly_balance(self):
        df = pd.read_csv(self.treasury_file)
        df['payment_date'] = pd.to_datetime(df['payment_date'])
        monthly_data = df.groupby([df['payment_date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        monthly_data['balance'] = monthly_data.get('I', 0) - monthly_data.get('E', 0)

        return pd.DataFrame({
            'month': monthly_data.index.astype(str),
            'balance': monthly_data['balance'].values
        })

    def delete_data(self,invoice_date,payment_date,company,description,amount,type):
        """Delete data from csv based on match the fields"""

        df = pd.read_csv(self.treasury_file)

        #Make sure the dates are in the same format as the DataFrame
        invoice_date = pd.to_datetime(invoice_date)
        payment_date = pd.to_datetime(payment_date)

        #Create a mask to match the record (the data will be true or false on this mask)

        mask=(
            (pd.to_datetime(df['invoice_date']) == invoice_date) &
            (pd.to_datetime(df['payment_date']) == payment_date) &
            (df['company'] == company) &
            (df['description'] == description) &
            (df['amount'] == amount) &
            (df['type'] == type)
        )

        #Delete the matching row saving the elements without true
        df = df[~mask]

        #Save the updated DataFrame to the .csv
        df.to_csv(self.treasury_file,index=False)

        #This return true if at least 1 row is deleted
        return sum(mask)>0

    def get_next_days(self,days = 30):
        """Get the balance to the next 30 days to graph"""

        df = pd.read_csv(self.treasury_file)
        # Make sure the date is a date type, not string
        df['payment_date'] = pd.to_datetime(df['payment_date'])

        #Get the date range
        today = datetime.now().date()
        next_days = today + timedelta(days=days)

        #Filter data on the range
        mask = (df['payment_date'].dt.date >= today) & (df['payment_date'].dt.date <= next_days)
        data_days = df[mask]

        if data_days.empty:
            empty_df = pd.DataFrame(index=pd.date_range(start=today, end=next_days))
            empty_df['I'] =0
            empty_df['E'] = 0
            return empty_df

        #Group by date and type, with the sum of amount, unstack separate the columns Expenses and Incomes
        daily_data = data_days.groupby(['payment_date', 'type'])['amount'].sum().unstack(fill_value=0)

        if 'E' not in daily_data.columns:
            daily_data['E'] = 0
        if 'I' not in daily_data.columns:
            daily_data['I'] = 0

        all_dates = pd.date_range(start=today, end = next_days)#Generate all dates between start and end
        daily_data = daily_data.reindex(all_dates,fill_value=0) #Make sure all dates have data

        return daily_data

    def get_quarter(self):
        """Get the balance to this quarter"""
        df = pd.read_csv(self.treasury_file)
        # Make sure the date is a date type, not string
        df['payment_date'] = pd.to_datetime(df['payment_date'])

        #Get the current quarter, start and end
        today = datetime.now()
        current_quarter = (today.month -1) // 3+1 #Actual month - 1 / number months +1
        first_month = 3 * current_quarter -2
        last_month = 3 * current_quarter

        start_date = datetime(today.year, first_month,1) #First day current quarter
        end_date = datetime(today.year, last_month + 1, 1) - timedelta(days=1) #Firt day next quarter less 1 day

        #Filter data for quarter
        mask = (df['payment_date']>= start_date) & (df['payment_date'] <= end_date)
        quarter_data = df[mask]

        if quarter_data.empty:
            months = pd.date_range(start=start_date, end=end_date, freq='ME').to_period('M')
            empty_df= pd.DataFrame(index=months)
            empty_df['I'] =0
            empty_df['E'] = 0
            return empty_df

        #Group by date(Month) and type, with the sum of amount, unstack separate the columns Expenses and Incomes
        monthly_data = quarter_data.groupby([quarter_data['payment_date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)

        #make suer this columns exists
        if 'E' not in monthly_data.columns:
            monthly_data['E'] = 0
        if 'I' not in monthly_data.columns:
            monthly_data['I'] = 0

        return monthly_data

    def get_year(self):
        """Get the balance to this year"""
        df = pd.read_csv(self.treasury_file)
        # Make sure the date is a date type, not string
        df['payment_date'] = pd.to_datetime(df['payment_date'])

        #Get the current year dates
        today = datetime.now()
        start_date = datetime(today.year, 1,1) #First day of year
        end_date = datetime(today.year,12, 31)  #Last day of year

        #Filter data for quarter
        mask = (df['payment_date']>= start_date) & (df['payment_date'] <= end_date)
        year_data = df[mask]

        if year_data.empty:
            months = pd.date_range(start=start_date, end=end_date, freq='ME').to_period('M')
            empty_df = pd.DataFrame(index=months)
            empty_df['I'] = 0
            empty_df['E'] = 0
            return empty_df

        #Group by date(Month) and type, with the sum of amount, unstack separate the columns Expenses and Incomes
        monthly_data = year_data.groupby([year_data['payment_date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)

        # make sure the columns exists
        if 'E' not in monthly_data.columns:
            monthly_data['E'] = 0
        if 'I' not in monthly_data.columns:
            monthly_data['I'] = 0

        return monthly_data


