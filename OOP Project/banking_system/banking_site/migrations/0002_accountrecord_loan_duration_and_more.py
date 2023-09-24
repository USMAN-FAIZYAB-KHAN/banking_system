# Generated by Django 4.2.2 on 2023-06-20 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrecord',
            name='loan_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='accountrecord',
            name='principle_amount',
            field=models.FloatField(null=True),
        ),
    ]
