from .checking_account import CheckingAccount
from .saving_account import SavingAccount
from .loan_account import LoanAccount
from .transaction import Transaction
from banking_site.models import CustomerRecord, TransactionRecord, AccountRecord

class Customer:
    # Contructor
    def __init__(self, username='', password='', first_name='', last_name='', address=''):
        #Attributes are private to make it preserved and save from illegal attack
        self.__username = username
        self.__password = password
        self.__first_name = first_name
        self.__last_name = last_name
        self.__address = address
        # these two bring lines all the transactions and accounts from the database
        # into the memory
        self.__transactions = self.get_transactions_from_DB()
        self.__accounts = self.get_accounts_from_DB()
    
    #getter and setter methods are used to used these private attributes    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password

    def get_first_name(self):
        return self.__first_name
    
    def get_transactions(self):
        return self.__transactions

    def get_last_name(self):
        return self.__last_name

    def get_address(self):
        return self.__address

    def get_accounts(self):
        return self.__accounts
    
    # To verify the password that user enter
    def verify_password(self, password):
        return self.__password == password

    def set_password(self, pwd):
        self.__password = pwd
    
    # Transaction Class composition with customer class
    def add_transaction(self, amount, account_number, transaction_type, account_type):
        # gettting the account id and customer id from the database
        act_id = AccountRecord.objects.get(account_num=account_number).id
        cust_id = CustomerRecord.objects.get(username=self.__username).id
        # creating the transaction object
        t =  Transaction(amount, account_number, transaction_type, account_type)
        # saving the transaction to the database
        t.save_to_db(account_id=act_id, customer_id=cust_id)
        # adding the transaction to the list of transactions of the customer
        self.__transactions.append(t) 

    #Checking Account composition with customer class
    def open_checking_account(self, balance=0, account_num='',account_pin='',credit_limit=10000):
        # creating the checking account object
        checking_account = CheckingAccount(balance, account_num, account_pin, credit_limit) 
        # getting the customer id from the database
        id = CustomerRecord.objects.get(username=self.__username).id
        # trying to save the checking account to the database
        try:
            checking_account.save_to_db(account_type="Checking", customer_id=id)
        except:
            return False
        else:
            # if the account is saved successfully, add the account to the list of accounts of the customer
            self.__accounts["Checking"].append(checking_account) 
            return True

    # Saving Account composition with customer class
    def open_saving_account(self,  balance=0, account_num="", account_pin="", interest_rate=10):
        saving_account = SavingAccount(balance, account_num, account_pin, interest_rate)
        id = CustomerRecord.objects.get(username=self.__username).id
        try:
            saving_account.save_to_db(account_type="Saving", customer_id=id)
        except:
            return False
        else:
            self.__accounts["Saving"].append(saving_account) 
            return True

        # Loan Account composition with customer class
    def open_loan_account(self,  balance=0, account_num="", account_pin="", principle_amount=0, loan_duration=0, interest_rate=22):
        loan_account = LoanAccount(balance, account_num, account_pin, principle_amount, loan_duration, interest_rate)
        id = CustomerRecord.objects.get(username=self.__username).id
        try:
            loan_account.save_to_db(account_type="Loan", customer_id=id, loan_duration=loan_duration, principle_amount=principle_amount)
        except:
            return False
        else:
            self.__accounts["Loan"].append(loan_account) 
            return True
        
    #The function of this method is to approach the data which are in database of django
     #It fetch the data from transaction table of database and store in the list.
    def get_transactions_from_DB(self):
        transactions = []
        if CustomerRecord.objects.filter(username=self.__username).exists():
            customer_id = CustomerRecord.objects.get(username=self.__username).id
            for t in TransactionRecord.objects.filter(customer=customer_id):
                #The data that we fetch from DB becomes object of transaction and append in the list
                transactions.append(Transaction(int(t.amount), t.account.account_num, t.transaction_type, t.account_type, t.transaction_date))
        return transactions
    
    #It fetch the data from Accounts table of database and store in the dictionary.
    def get_accounts_from_DB(self):
        #Inside dictionary we have list as values for checking, saving and loan accounts respectively
        #Inside the list we store objects of accounts for specific user.
        accounts = {"Checking": [], "Saving": [], "Loan": []}
        if CustomerRecord.objects.filter(username=self.__username).exists():
            customer_id = CustomerRecord.objects.get(username=self.__username).id
            for a in AccountRecord.objects.filter(customer=customer_id):
                if a.account_type == "Checking":
                    accounts["Checking"].append(CheckingAccount(balance=int(a.balance), account_num=a.account_num, account_pin=a.account_pin, creation_date=a.creation_date))
                elif a.account_type == "Saving":
                    accounts["Saving"].append(SavingAccount(balance=int(a.balance), account_num=a.account_num, account_pin=a.account_pin, creation_date=a.creation_date))
                elif a.account_type == "Loan":
                    accounts["Loan"].append(LoanAccount(balance=int(a.balance), account_num=a.account_num, account_pin=a.account_pin, creation_date=a.creation_date, principle_amount=int(a.principle_amount), loan_duration=a.loan_duration))
        return accounts

    #This method is used to save all the data of customer in database
    def save_to_db(self):
        c = CustomerRecord(username=self.__username, password=self.__password, first_name=self.__first_name, last_name=self.__last_name, address=self.__address)
        c.save()