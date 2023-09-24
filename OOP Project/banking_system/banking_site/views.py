from django.shortcuts import render, redirect
from classes.bank import *
from classes.admin import *
from datetime import datetime,timedelta
import uuid
from banking_site.models import AccountRecord
# Create your views here.
# Create a bank object
b = Bank("Bank of Pakistan", "123 Main St, New York, NY 10001")
# Create an admin object associated with the bank
admin = Admin("admin", "12345678", b.get_customers())
# initialize the global customer variable to None 
customer = None

def home(request):
    # Check if the user is logged in then logout the user
    global customer
    if customer:
        customer = None
    return render(request, 'home.html', {'home': True})

def login(request):
    if request.method == "POST":
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        for c in b.get_customers():
            # Check if the username and password are correct
            if c.get_username() == username and c.verify_password(password):
                global customer
                # Set the global customer variable to the current customer
                customer = c
                # Redirect to the user home page
                # Check if the interest needs to be added to the accounts
                alerts = []
                interest_accounts = []
                # get the accounts of the customer which have interest
                for acc_type in c.get_accounts():
                    for account in c.get_accounts()[acc_type]: 
                        # if the account is a saving account, get the last interest addition date
                        # and append the account to the interest_accounts list
                        if acc_type == "Saving":
                            acnt_num = account.get_account_number()
                            date = AccountRecord.objects.get(account_num = acnt_num).last_interest_addition_date
                            interest_accounts.append((account.get_account_number(), date, acc_type, account.balance_inquiry(), account.get_interest_rate()))

                        elif acc_type == "Loan":
                            # if the account type is loan, then find the latest transaction date on which loan was taken
                            # by reversing the list of transactions and finding the first transaction of type loan
                            transactions = []
                            # get the transactions of the customer
                            for transaction in customer.get_transactions():
                                if transaction.get_account_number() == account.get_account_number():
                                    Interest_date = AccountRecord.objects.get(account_num = account.get_account_number()).last_interest_addition_date
                                    transactions.append({'type': transaction.get_transaction_type(), 'date': transaction.get_transaction_date(), 'interest_date': Interest_date})
                            # sort the transactions by date
                            transactions.sort(key=lambda x: x['date'], reverse=True)
            
                            for transaction_ in transactions:
                                if transaction_["type"] == "Loan":
                                    date = transaction_["interest_date"]
                            interest_accounts.append((account.get_account_number(), date, acc_type, account.balance_inquiry(), account.get_interest_rate()))
            
                # add interest to the accounts if the last interest addition date is more than { 1 minute } ago
                for account in interest_accounts:
                    acc_num = account[0] 
                    date = account[1]
                    acc_type = account[2] 

                    # if the last interest addition date is more than 1 minute ago, set the interest_status to True
                    # We set the time interval to 1 month by changing the timedelta(minutes=1) to timedelta(days=30)
                    if timedelta(minutes=1) <= datetime.now() - date:
                        AccountRecord.objects.filter(account_num=acc_num).update(interest_status = True)

                    # if the interest_status is True, add the interest to the account
                    if AccountRecord.objects.get(account_num= acc_num).interest_status == True:
                        interest = round(account[3] * account[4] / 100)
                        print("Interest: ", interest)
                        if interest != 0:
                            alerts.append({'account_num': account[0], 'interest': interest, 'rate': account[4]})
                        AccountRecord.objects.filter(account_num=acc_num).update(interest_status = False)
                        AccountRecord.objects.filter(account_num=acc_num).update(last_interest_addition_date=datetime.now())
                        
                        # add the interest to the account 
                        for acnt in c.get_accounts()[acc_type]: 
                            if acnt.get_account_number() == acc_num:
                                acnt.add_interest()
                                # update the last interest addition date in the database
                                AccountRecord.objects.filter(account_num=acc_num).update(last_interest_addition_date=datetime.now())
                                AccountRecord.objects.filter(account_num=acc_num).update(balance=acnt.balance_inquiry())
                
                request.session['alerts'] = alerts
                return redirect('user_home') 
        # if the username and password are incorrect, render the login page with an error message 
        return render(request, 'login.html', {'error': 'Invalid username or password', 'login': True})        
    return render(request, 'login.html', {'login': True})

def signup(request):
    if request.method == "POST":
        # Get the username, password, first name, last name, and address from the form
        name = request.POST.get('name')
        password = request.POST.get('password')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address = request.POST.get('address')
        for customer in b.get_customers():
            if customer.get_username() == name:
                # If the username already exists, render the signup page with an error message
                return render(request, 'signup.html', {'error': 'Username already exists', 'signup': True})

        # if the username does not exist, create and save the customer object to the database and redirect to the login page
        c = Customer(name, password, first_name, last_name, address)
        # add the customer to the bank's list of customers
        b.add_customer(c)
        # save the customer to the database
        c.save_to_db()    
        # redirect to the login page
        return redirect('login')
    return render(request, 'signup.html', {'signup': True})

def admin_login(request):
    if request.method == "POST":
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the username and password are correct
        if username == admin.get_username() and admin.verify_password(password):
            # Redirect to the admin home page
            return redirect('admin_home')
        # if the username and password are incorrect, render the admin login page with an error message
        return render(request, 'admin_login.html', {'error': 'Invalid username or password', 'admin_login': True})
    return render(request, "admin_login.html", {'admin_login': True})

def admin_home(request):
    total_customers = len(admin.get_bank_customers())
    total_accounts = 0 
    total_transactions = 0
    # get the total number of accounts and transactions
    for c in admin.get_bank_customers():
        total_transactions += len(c.get_transactions())
        for acc_type in c.get_accounts():
            total_accounts += len(c.get_accounts()[acc_type])

    customers = []
    # if the request method is POST, get the name from the form and search for the customer
    if request.method == "POST":
        name = request.POST.get('name_search')
        for c in admin.get_bank_customers():
            # if the name is in the customer's username, add the customer to the list of customers
            if name.lower() in c.get_username().lower():
                customers.append(c.get_username())
    else:
        # if the request method is GET, add all the customers to the list of customers
        for c in admin.get_bank_customers():
            customers.append(c.get_username())
    customers.sort()
    # render the admin home page with the list of customers
    return render(request, 'admin.html', {'customers': customers, 'total_customers': total_customers, 'total_accounts': total_accounts, 'total_transactions': total_transactions, 'admin_home': True})

def admin_accounts(request, username):
    customers = []
    # if the request method is POST, get the name from the form and search for the customer
    if request.method == "POST":
        name = request.POST.get('name_search')
        for c in admin.get_bank_customers():
            # if the name is in the customer's username, add the customer to the list of customers
            if name.lower() in c.get_username().lower():
                customers.append(c.get_username())
    else:
        # if the request method is GET, add all the customers to the list of customers
        for c in admin.get_bank_customers():
            customers.append(c.get_username())
    # render the homepage with the information of the customer
    context = admin.print_report(username)
    context['customers'] = sorted(customers)
    context['display'] = True
    return render(request, 'admin.html', context) 
    
def admin_transactions_view(request, name, account_num):
    transactions = []
    # get the balance of the account
    for c in admin.get_bank_customers():
        if c.get_username() == name:
            for account_type in c.get_accounts():
                for account in c.get_accounts()[account_type]:
                    if account.get_account_number() == account_num:
                        act_type = account_type
                        balance = account.balance_inquiry()

                        if account_type == 'Checking':
                            credit_limit = account.get_credit_limit()
                            if balance < 0:
                                remaining_credit_limit = credit_limit + balance
                                balance = 0
                            else:
                                remaining_credit_limit = credit_limit

                        else:
                            interest_rate = account.get_interest_rate() 
                            if account_type == "Loan":
                                principle_amount = account.get_principle_amount()
                                loan_dur = account.get_loan_duration()


    # get the transactions of the account
    for c in admin.get_bank_customers():
        if c.get_username() == name:
            for transaction in c.get_transactions():
                if transaction.get_account_number() == account_num:
                    transactions.append({'type': transaction.get_transaction_type(), 'amount': transaction.get_amount(), 'date': transaction.get_transaction_date()})
    # sort the transactions by date
    transactions.sort(key=lambda x: x['date'], reverse=True)

    if act_type == 'Checking':
        return render(request, 'transactions.html', {'transactions': transactions, 'account_number': account_num, 'balance': balance, 'username': name, 'remaining_credit_limit': remaining_credit_limit, 'account_type': act_type, 'credit_limit': credit_limit})
    # render the transactions page with the transactions and balance
    elif act_type == 'Loan':
        return render(request, 'transactions.html', {'transactions': transactions, 'account_number': account_num, 'balance': balance, 'username': name, 'principle_amount': principle_amount, 'account_type': act_type, 'interest_rate': interest_rate, 'loan_duration': loan_dur})
    else:
        return render(request, 'transactions.html', {'transactions': transactions, 'account_number': account_num, 'balance': balance, 'username': name, 'interest_rate': interest_rate, 'account_type': act_type})


def user_home(request):
    # calculate the total number of accounts of the logged in customer
    total_accounts = 0
    for account_type in customer.get_accounts():
        total_accounts += len(customer.get_accounts()[account_type])
   
    alerts = request.session.get('alerts')
    if alerts:
        request.session['alerts'] = None
        return render(request, 'user_home.html', {'username': customer.get_username(), 'first_name': customer.get_first_name(), 'last_name': customer.get_last_name(), 'total_accounts': total_accounts, 'address': customer.get_address(), 'alerts': alerts})

    # render the user home page with the information of the logged in customer
    return render(request, 'user_home.html', {'username': customer.get_username(), 'first_name': customer.get_first_name(), 'last_name': customer.get_last_name(), 'total_accounts': total_accounts, 'address': customer.get_address()})


def show(request):
    selected_accounts = []
    # get the account type from the url
    msg = request.GET.get('msg')

    account_type = request.GET.get('param1')
    # get the accounts of the customer of the specified account type
    title = account_type + ' Accounts'
    accounts = customer.get_accounts()
    for account in accounts[account_type]:
        account_num = account.get_account_number()
        creation_date = account.get_creation_date()
        # add the account to the list of accounts
        selected_accounts.append({'account_type':account_type,'account_num':account_num,'creation_date':creation_date})
    # render the show page with the list of accounts
    if msg:
        return render(request,'show.html', {'accounts':selected_accounts, 'account_type': account_type, 'title':title, 'msg':msg})
    return render(request,'show.html', {'accounts':selected_accounts, 'account_type': account_type, 'title':title})

def generate_account_number(account_type):
    # generate a random account number of the specified account type
    account_number = account_type + str(uuid.uuid4().int)[:4]
    return account_number

def account_creation(request):
    if request.method == 'POST':
        # get the account type and pin from the form
        pin = request.POST.get('pin')
        account_type = request.POST.get('acc_type')
        # create the account and generate the account number of the specified account type

        if account_type == 'Saving':
                account_num = generate_account_number('SA')
                success = customer.open_saving_account(account_num=account_num, account_pin=pin)
                # if the account is created successfully, update the last interest addition date of the account for adding interest
                AccountRecord.objects.filter(account_num=account_num).update(last_interest_addition_date=datetime.now())

        elif account_type == 'Checking':
                account_num = generate_account_number('CA')
                success = customer.open_checking_account(account_num=account_num, account_pin=pin)
        
        elif account_type == 'Loan':
                account_num = generate_account_number('LA')
                success = customer.open_loan_account(account_num=account_num, account_pin=pin)
        # if the account is created successfully, render the account creation page with the account number
        if success:
            msg = f"Account created successfully. Your account number is {account_num}"
            redirected_url = f"http://127.0.0.1:8000/user_accounts/?param1={account_type}&msg={msg}"
            return redirect(redirected_url)

        # if the account is not created successfully, render the account creation page with an error message
        else:
            return render(request, 'setpin.html', {'error': 'Account creation failed'})
    return render(request,'setpin.html') 

def account_verification(request, account_number):
    if request.method == 'POST':
        # get the pin from the form
        pin = request.POST.get('pin')
        # check if the pin is correct
        for account_type in customer.get_accounts():
            for account in customer.get_accounts()[account_type]:
                if account.get_account_number() == account_number:
                    if account.verify_pin(pin):
                        # if the pin is correct, redirect to the account details page
                        return redirect("account_detail", account_type=account_type, acnt_num=account_number)
                    else:
                        # if the pin is incorrect, render the account verification page with an error message
                        return render(request, 'Verifypin.html', {'error': 'Account not verified', 'account_num': account_number})
    return render(request, 'Verifypin.html', {'account_num': account_number})

def account_details(request, account_type, acnt_num):
    transactions = []
    # get the account details of the specified account type and account number
    for account in customer.get_accounts()[account_type]:
        if account.get_account_number() == acnt_num:
            balance = account.balance_inquiry()

            # if the balnce is negative, set it to 0 only for displaying it
            # will remain negative in the database
            if balance < 0:
                balance = 0
        
            creation_date = account.get_creation_date()
            
            # get the transactions of the account
            for transaction in customer.get_transactions():
                if transaction.get_account_number() == acnt_num:
                    transactions.append({'type': transaction.get_transaction_type(), 'amount': transaction.get_amount(), 'date': transaction.get_transaction_date()})
            
            # sort the transactions by date and an anonymous function is passed as the key to sort the transactions by date
            transactions.sort(key=lambda x: x['date'], reverse=True)

            if account_type == "Checking":
                if account.balance_inquiry() < 0:
                    # if the account is a checking account and the balance is negative, get the overdraft limit
                    remaining_credit_limit = account.get_credit_limit() + account.balance_inquiry()
                else:
                    remaining_credit_limit = account.get_credit_limit()
                # render the account details page with the account details
                return render(request, 'account_detail.html', {'account_type': account_type, 'account_num': acnt_num, 'balance': balance, 'creation_date': creation_date, 'credit_limit': account.get_credit_limit(),'remaining_credit_limit': remaining_credit_limit, 'transactions': transactions, 'display': True})
            
            # if the account is a loan account, get the loan duration and principle amount
            if account_type == "Loan":
                loan_duration = account.get_loan_duration()
                principle_amount = account.get_principle_amount()
                interest = account.get_interest_rate()
                # render the account details page with the account details
                return render(request, 'account_detail.html', {'account_type': account_type, 'account_num': acnt_num, 'balance': balance, 'creation_date': creation_date, 'loan_duration': loan_duration, 'principle_amount': principle_amount, 'transactions': transactions, 'interest_rate': interest , 'display': True})

    interest = account.get_interest_rate()      
    return render(request, 'account_detail.html', {'account_type': account_type, 'account_num': acnt_num, 'balance': balance, 'creation_date': creation_date, 'transactions': transactions, 'display': True, 'interest_rate': interest})

def account_deposit(request, account_type, acnt_num):
    # Get the balance of the account
    for acnt in customer.get_accounts()[account_type]:
        if acnt.get_account_number() == acnt_num:
            balance = acnt.balance_inquiry()
            # if the balance is negative, set it to 0 only for displaying purposes only
            if account_type == "Checking":
                if balance < 0:
                    # Calculate the remaining credit limit
                    remaining_credit_limit = acnt.get_credit_limit() + balance
                    balance = 0
                else:
                    remaining_credit_limit = acnt.get_credit_limit()

    # if the request method is POST, get the amount from the form
    if request.method == 'POST':
        amount = request.POST.get('amount')
        amount = int(amount)
        # find the account of the specified account type and account number
        for a in customer.get_accounts()[account_type]:
            if a.get_account_number() == acnt_num:
                account = a

        # if the amount is deposited successfully, render the deposit page with the new balance and the success message
        # else render the deposit page with the error message
        success, msg = account.deposit(amount)
        # if the balance is negative, set it to 0 only for displaying purposes only
        balance = account.balance_inquiry()
        if account_type == "Checking": 
            if balance < 0:
                remaining_credit_limit = account.get_credit_limit() + balance
                balance = 0
            else:
                remaining_credit_limit = account.get_credit_limit()

        if success:
            if account_type == "Loan":
                customer.add_transaction(amount=amount, account_number=acnt_num, transaction_type="Loan Payment", account_type=account_type)
                b.add_transaction(account_number=acnt_num, transaction_type= "Loan Payment", account_type=account_type , amount=amount)
            else:
                customer.add_transaction(amount=amount, account_number=acnt_num, transaction_type="Deposit", account_type=account_type)
                b.add_transaction(account_number=acnt_num, transaction_type="Deposit", account_type=account_type , amount=amount)
            if account_type == "Checking":
                return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, 'remaining_credit_limit': remaining_credit_limit, "success": msg})
            return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, "success": msg})            
        else:
            if account_type == "Checking":
                return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, 'remaining_credit_limit': remaining_credit_limit, "error": msg})
            return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, "error": msg})
    
    if account_type == "Checking":
        return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, 'remaining_credit_limit': remaining_credit_limit})
    return render(request, 'deposit.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance})

def account_withdraw(request, account_type, acnt_num):
    # get the balance of the account
    for acnt in customer.get_accounts()[account_type]:
        if acnt.get_account_number() == acnt_num:
            balance = acnt.balance_inquiry()
            # if the balance is negative, set it to 0 only for displaying purposes only
            if account_type == "Checking":
                if balance < 0:
                    # Calculate the remaining credit limit
                    remaining_credit_limit = acnt.get_credit_limit() + balance
                    balance = 0
                else:
                    remaining_credit_limit = acnt.get_credit_limit()

    if request.method == 'POST':
        # get the amount from the form
        amount = request.POST.get('amount')
        amount = int(amount)
        for a in customer.get_accounts()[account_type]:
            if a.get_account_number() == acnt_num:
                account = a

        # if the amount is withdrawn successfully, render the withdraw page with the new balance and the success message
        # else render the withdraw page with the error message
        e = account.withdraw(amount)
        success, msg = e
        balance = account.balance_inquiry()
        if account_type == "Checking": 
            if balance < 0:
                remaining_credit_limit = account.get_credit_limit() + balance
                balance = 0
            else:
                remaining_credit_limit = account.get_credit_limit()

        if success:
                AccountRecord.objects.filter(account_num=acnt_num).update(balance=account.balance_inquiry())
                customer.add_transaction(amount=amount, account_number= acnt_num, transaction_type='Withdraw', account_type=account_type)
                b.add_transaction(amount=amount, account_number= acnt_num, transaction_type='Withdraw', account_type=account_type)

        if account_type == "Checking":
            return render(request, 'withdraw.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, 'balance': balance, 'remaining_credit_limit': remaining_credit_limit, "success": success, 'msg':msg})
        return render(request, 'withdraw.html', {'account_type': account_type, 'account_num': acnt_num, 'display': True, "success": success, 'msg':msg, 'balance': balance})
    
    if account_type == "Checking":
        return render(request, 'withdraw.html', {'account_type': account_type, 'account_num': acnt_num,'display': True, 'balance': balance, 'remaining_credit_limit': remaining_credit_limit})
    return render(request, 'withdraw.html', {'account_type': account_type, 'account_num': acnt_num,'display': True, 'balance': balance})

def take_loan(request, act_type, act_num):
    for account in customer.get_accounts()[act_type]:
        if account.get_account_number() == act_num:
            principle_amount = account.get_principle_amount()
            balance = account.balance_inquiry()
            # if the loan is already taken, render the take loan page with the error message
            if balance > 0  and principle_amount > 0:
                return render(request, 'take_loan.html', {"account_type": act_type, "account_num": act_num, "display": True, "error": "You already have a loan"})
            
    # get the amount and duration from the option which the user selected
    amount = request.GET.get('amount')
    duration = request.GET.get('duration')

    # if the amount and duration are not None, set the principle amount and duration of the account
    if amount != None and duration != None:
        duration = int(duration)
        amount = int(amount)
        for account in customer.get_accounts()[act_type]:
            if account.get_account_number() == act_num:
                account.set_principle_amount(amount)
                account.set_loan_duration(duration) 
                account.set_balance(amount)
                # update the database with the new principle amount, duration and balance
                AccountRecord.objects.filter(account_num=act_num).update(principle_amount=amount, loan_duration=duration)
                AccountRecord.objects.filter(account_num=act_num).update(last_interest_addition_date = datetime.now())
                AccountRecord.objects.filter(account_num=act_num).update(balance=account.balance_inquiry())

                # add the loan transaction to the customer and bank
                customer.add_transaction(amount=amount, account_number=act_num, transaction_type="Loan", account_type=act_type)
                b.add_transaction(amount=amount, account_number=act_num, transaction_type="Loan", account_type=act_type)

                # render the take loan page with the success message
                return render(request, 'take_loan.html', {"account_type": act_type, "account_num": act_num, "display": True, "success": "Loan taken successfully"})
    return render(request, 'take_loan.html', {"account_type": act_type, "account_num": act_num, "display": True}) 