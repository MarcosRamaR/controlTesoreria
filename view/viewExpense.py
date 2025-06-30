# viewExpense.py
from view.viewTransactions import BaseTransactionView

class ExpensesView(BaseTransactionView):
    def __init__(self, frame, update_callback=None):
        super().__init__(frame, 'E', "Expense", update_callback)

