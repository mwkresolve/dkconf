# Generated by Django 4.0.1 on 2022-11-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefinances', '0002_alter_walletbank_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='walletbitcoin',
            name='balance',
        ),
        migrations.AlterField(
            model_name='walletbank',
            name='balance',
            field=models.FloatField(),
        ),
    ]
