from django.db import models
from controller.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class WalletBitcoin(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    # balance = models.FloatField(default=1.0)
    balance = models.DecimalField(max_digits=13, decimal_places=8, validators=[
                                      MinValueValidator(Decimal('0.00000000'))],
                                  default=Decimal('1.00000001'))


class WalletBank(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('10000.00'))


