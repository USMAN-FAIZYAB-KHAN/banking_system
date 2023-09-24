from .account import Account
from banking_site.models import AccountRecord
import datetime

class LoanAccount(Account):

    def __init__(self, balance=0, account_num="", account_pin="", principle_amount=0, loan_duration=0, interest_rate=22, creation_date=None):
        super().__init__(balance, account_num, account_pin, creation_date)
        self.__principle_amount = principle_amount
        self.__loan_duration = loan_duration
        self.__interest_rate = interest_rate

    def deposit(self, amount):
        # check if the amount is less than or equal to 0 
        if amount <= 0:
            return False, "Invalid deposit amount" 
        # check if the user has already paid off the loan
        elif self._balance == 0:
            return False, "You have already paid off your loan."
        # check if the amount to be deposited is more than the balance
        elif self._balance < amount:
            return False, "You cannot deposit more than the balance of the  account. "
        else:
            # deduct the amount from the balance
            self._balance -= amount
            # update the balance in the database
            AccountRecord.objects.filter(account_num=self._account_num).update(balance=self._balance)
            return True, "Amount Deposited Successfully!"
        
    def set_principle_amount(self, principle_amount):
        self.__principle_amount = principle_amount

    def set_loan_duration(self, loan_duration):
        self.__loan_duration = loan_duration

    def get_principle_amount(self):
        return self.__principle_amount

    def get_interest_rate(self):
        return self.__interest_rate

    def get_loan_duration(self):
        return self.__loan_duration

    def add_interest(self):
        # add the interest to the balance
        factor = self.__interest_rate/100
        self._balance += round(factor * self._balance)

