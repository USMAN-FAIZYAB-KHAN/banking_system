from .customer import Customer
from banking_site.models import CustomerRecord, TransactionRecord
from .transaction import Transaction

class Bank:
    def __init__(self, name='', address=''):
        self.__name = name
        self.__address = address
        # when we initialize the bank object, we read all the customers and transactions from the database, and when
        # customer object are initialized, they read all the accounts and transactions from the database
        # in this way a single object initialization of bank class will bring all the data we need in the memory
        self.__customers = self.read_customers_from_DB()
        self.__transactions = self.read_transactions_from_DB()

    def get_customers(self):
        return self.__customers

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_transactions(self):
        return self.__transactions

    def add_customer(self, c: Customer):
        self.__customers.append(c)
        
    def add_transaction(self, amount, account_number, transaction_type, account_type):
        # creating the transaction object
        t =  Transaction(amount, account_number, transaction_type, account_type)
        # appending the transaction to the record of the bank
        self.__transactions.append(t) 
    
    def read_customers_from_DB(self):
        # this method reads all the customers from the database and returns a list of customers objects
        customers = []
        for c in CustomerRecord.objects.all():
            customers.append(Customer(c.username, c.password, c.first_name, c.last_name, c.address))
        return customers

    def read_transactions_from_DB(self):
        # this method reads all the transactions from the database and returns a list of transactions objects
        transactions = []
        for t in TransactionRecord.objects.all():
            transactions.append(Transaction(int(t.amount), t.account.account_num, t.transaction_type, t.account_type, t.transaction_date))  
        return transactions
 