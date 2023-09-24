# Generated by Django 4.2.2 on 2023-07-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_site', '0006_alter_accountrecord_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrecord',
            name='interest_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='accountrecord',
            name='last_interest_addition_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
