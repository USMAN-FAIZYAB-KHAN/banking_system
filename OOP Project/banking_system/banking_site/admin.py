from django.contrib import admin
from .models import CustomerRecord, AccountRecord, TransactionRecord
# Register your models here.
admin.site.register(CustomerRecord)
admin.site.register(AccountRecord)
admin.site.register(TransactionRecord)