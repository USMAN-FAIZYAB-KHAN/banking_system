from banking_site.models import TransactionRecord
import datetime

class Transaction:
    def __init__(self, amount = 0, account_number: str = '', transaction_type: str = '',
                 account_type: str = '',  transaction_date=None):
        #Attributes are private to make it preserved and save from illegal attack
        self.__amount = amount
        self.__account_number = account_number
        self.__transaction_type = transaction_type 
        self.__account_type = account_type
        
        #This block is used to associate transaction date by using datetime module
        if transaction_date == None:
            self.__transaction_date = datetime.datetime.now()
        else:
            self.__transaction_date = transaction_date

    def get_amount(self):
        return self.__amount

    def get_account_number(self): 
        return self.__account_number

    def get_transaction_date(self):
        return self.__transaction_date

    def get_transaction_type(self):
        return self.__transaction_type

    def get_account_type(self):
        return self.__account_type
    
     #This method is used to save all the data related to transaction into the database
    def save_to_db(self, account_id, customer_id):
        transaction_record = TransactionRecord(account_id=account_id, customer_id=customer_id, amount=self.__amount, transaction_type=self.__transaction_type, account_type=self.__account_type, transaction_date=self.__transaction_date )
        transaction_record.save()
