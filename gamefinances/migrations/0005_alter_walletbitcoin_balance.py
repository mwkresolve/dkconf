# Generated by Django 4.0.1 on 2022-11-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefinances', '0004_alter_walletbitcoin_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletbitcoin',
            name='balance',
            field=models.DecimalField(decimal_places=7, max_digits=11),
        ),
    ]
