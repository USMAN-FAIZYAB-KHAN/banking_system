from abc import ABC, abstractmethod
# AccountRecord is present in the models.py file
from banking_site.models import AccountRecord
import datetime

class Account(ABC):

    def __init__(self, balance=0, account_num="", account_pin="", date=None):
        self._balance = balance
        self._account_num = account_num
        self._account_pin = account_pin
        # check if the date is not None
        if date != None:
            # set the creation date to the date passed in
            self._creation_date = date
        else:
            # set the creation date to the current date
            self._creation_date = datetime.datetime.now() 
    
    # this is an abstract method
    @abstractmethod
    def deposit(self, amount):
        pass

    def withdraw(self, amount):
                # check if the amount is less than or equal to 0
        if amount <= 0:
            return False, "Invalid deposit amount"

        # check if the balance is less than or equal to 0
        if self._balance <= 0:
            # return false and a message
            msg = "Insufficient balance"
            # this boolean value and message is used in views.py file to take the appropriate action
            # and the message is displayed to the user
            return False, msg
        else:
            # check if the amount to be withdrawn is less than or equal to the balance
            if self._balance >= amount:
                # deduct the amount from the balance
                self._balance -= amount
                # return true and a message
                msg = "Amount withdrawn successfully"
                return True, msg
            # if the amount to be withdrawn is greater than the balance
            else:
                return False, "Insufficient balance"

    def get_creation_date(self):
        return self._creation_date
    
    
    def set_balance(self, balance):
        self._balance = balance

    
    def balance_inquiry(self):
        # check if the balance is an integer used only for display purposes
        return self._balance

    def get_account_number(self):
        return self._account_num

    def verify_pin(self, pin):
       # check if the pin passed in is equal to the account pin
       return pin == self._account_pin

    def save_to_db(self, account_type, customer_id, loan_duration=0, principle_amount=0):
        # check if the account type is loan
        if account_type == "Loan":
            # create a new account record with the loan duration and principle amount
            account_record = AccountRecord(account_num=self._account_num, balance=self._balance, account_type=account_type, account_pin=self._account_pin, customer_id=customer_id, loan_duration=loan_duration, principle_amount=principle_amount, creation_date=self._creation_date)
        else:
            # create a new account record without the loan duration and principle amount
            account_record = AccountRecord(account_num=self._account_num, balance=self._balance, account_type=account_type, account_pin=self._account_pin, customer_id=customer_id, creation_date=self._creation_date)
        # save the account record to the database
        account_record.save()
 