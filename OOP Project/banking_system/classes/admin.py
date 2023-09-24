class Admin:
    def __init__(self, username="", password="", customers=None):
        self.__username = username
        self.__password = password
        self.__bank_customers = customers

    # this method collects all the accounts and information of the customer passed as a parameter
    # and returns it as a dictionary object so that it can be displayed on the admin page
    def print_report(self, username):
            checking_accounts = []
            saving_accounts = []
            loan_accounts = []
            # finding the customer object in the list of customers
            for c in self.get_bank_customers():
                if c.get_username() == username:
                    user = c
                    no_of_accounts = 0
                    accounts = user.get_accounts()
                    for account_type in accounts:
                        for account in accounts[account_type]:
                            no_of_accounts += 1
                            if account_type == "Checking":
                                # if the balance is negative, we set it to zero only for the display purpose
                                balance = account.balance_inquiry()
                                if balance < 0:
                                    balance = 0
                                checking_accounts.append({'account_num': account.get_account_number(), 'balance': balance, 'creation_date': account.get_creation_date()})
                            elif account_type == "Saving":
                                saving_accounts.append({'account_num': account.get_account_number(), 'balance': account.balance_inquiry(), 'creation_date': account.get_creation_date()})
                            elif account_type == "Loan":
                                loan_accounts.append({'account_num': account.get_account_number(), 'balance': account.balance_inquiry(), 'creation_date': account.get_creation_date(), 'principle_amount': account.get_principle_amount(), 'loan_duration': account.get_loan_duration()})
            return {'username': user.get_username(), 'first_name': user.get_first_name(), 'last_name': user.get_last_name(), 'address': user.get_address(),'no_of_accounts': no_of_accounts, 'checking_accounts': checking_accounts, 'saving_accounts': saving_accounts, 'loan_accounts': loan_accounts}

    def get_bank_customers(self):
        return self.__bank_customers

    def get_username(self):
        return self.__username

    def verify_password(self, pwd):
        return self.__password == pwd

    def set_password(self, pwd):
        self.__password = pwd

    def set_bank(self, customers):
        self.__bank_customers = customers