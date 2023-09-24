from django.db import models

# Create your models here.
class CustomerRecord(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username

class AccountRecord(models.Model):
    customer = models.ForeignKey(CustomerRecord, on_delete=models.CASCADE)
    balance = models.FloatField()
    account_num = models.CharField(max_length=50)
    account_pin = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)
    creation_date = models.DateTimeField(blank=True, null=True)
    loan_duration = models.IntegerField(null=True, blank=True)
    principle_amount = models.FloatField(null=True, blank=True)
    last_interest_addition_date = models.DateTimeField(null=True, blank=True)
    interest_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.account_num

class TransactionRecord(models.Model):
    account = models.ForeignKey(AccountRecord, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerRecord, on_delete=models.CASCADE)
    amount = models.FloatField() 
    transaction_date = models.DateTimeField(null=True, blank=True)
    transaction_type = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.transaction_type