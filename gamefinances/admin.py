from django.contrib import admin
from .models import WalletBitcoin, WalletBank

# Register your models here.
admin.site.register(WalletBitcoin)

admin.site.register(WalletBank)

