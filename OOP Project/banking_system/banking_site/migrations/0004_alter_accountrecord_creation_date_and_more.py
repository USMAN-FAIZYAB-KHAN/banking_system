# Generated by Django 4.2.2 on 2023-07-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_site', '0003_accountrecord_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrecord',
            name='creation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='transaction_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
