from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Processes, User
from datetime import timedelta, date, datetime
from controller.functionsdb import *
from .models import *


class FinancesView(TemplateView):
    template_name = "finances.html"

    def get(self, request, *args):
        btc_wallet = WalletBitcoin.objects.filter(userid=request.user).values()[0]
        bank_wallet = WalletBank.objects.filter(userid=request.user).values()[0]
        # get get_btc_value() esta atrasando o carregamento da pagina
        # value_btc = get_btc_value()
        return render(request, self.template_name, {'btc_wallet': btc_wallet, 'bank_wallet':bank_wallet })

