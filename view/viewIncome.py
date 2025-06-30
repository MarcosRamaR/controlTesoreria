# viewIncome.py
from view.viewTransactions import BaseTransactionView

class IncomesView(BaseTransactionView):
    def __init__(self, frame, update_callback=None):
        super().__init__(frame, 'I', "Income", update_callback)