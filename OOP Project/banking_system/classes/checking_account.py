from .account import Account
from banking_site.models import AccountRecord

class CheckingAccount(Account):

    def __init__(self, balance=0, account_num="", account_pin="", credit_limit=10000, creation_date=None):
        super().__init__(balance, account_num, account_pin, creation_date)
        self.__credit_limit = credit_limit

    def deposit(self, amount):
        # check if the amount is less than or equal to 0
        if amount <= 0:
            return False, "Invalid deposit amount"
        # add the amount to the balance
        self._balance += amount
        # update the balance in the database
        AccountRecord.objects.filter(account_num=self._account_num).update(balance=self._balance)
        return True, "Amount Deposited Successfully!"


    def withdraw(self, amount):
        if amount <= 0:
            return False, "Invalid withdrawal amount"

        # check if the amount to be deposited is less than or equal to the balance
        if self._balance >= amount:
            # deduct the amount from the balance
            self._balance -= amount
            # update the balance in the database
            AccountRecord.objects.filter(account_num=self._account_num).update(balance=self._balance)
            # return true and a message
            return True, "Amount Withdrawn Successfully!"
        
      
        # check if the amount to be withdrawn is less than or equal to the balance + credit limit
        if amount <= self.__credit_limit + self._balance:
            self._balance -= amount 
            return True, "Amount Withdrawn Successfully!"

        return False, "Insufficient funds and credit limit"
    
    def get_credit_limit(self):
        return self.__credit_limit
