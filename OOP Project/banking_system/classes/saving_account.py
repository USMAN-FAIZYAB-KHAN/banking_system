from .account import Account
from banking_site.models import AccountRecord 
import datetime
class SavingAccount(Account):

    def __init__(self, balance=0, account_num="", account_pin="", interest_rate=10, creation_date=None):
        super().__init__(balance, account_num, account_pin, creation_date)
        self.__interest_rate = interest_rate

    def deposit(self, amount):
        # if the amount is less than or equal to 0
        if amount <= 0:
            return False, "Invalid deposit amount"
        # add the amount to the balance
        self._balance += amount
        # update the balance in the database
        AccountRecord.objects.filter(account_num=self._account_num).update(balance=self._balance)
        return True, "Amount Deposited Successfully!"

    def get_interest_rate(self):
        return self.__interest_rate
    
    # this method is called after a specified period of time in the views.py file
    def add_interest(self):
        # add the interest to the balance
        factor = self.__interest_rate/100
        self._balance += round(factor * self._balance)
