from django.db import models
from controller.models import User


class WalletBitcoin(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    balance = models.DecimalField(decimal_places=7, max_digits=11)


class WalletBank(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    balance = models.FloatField()

