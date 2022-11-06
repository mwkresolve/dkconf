from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *
from django.views.generic import TemplateView, CreateView


class FinancesView(CreateView):
    template_name = "finances.html"

    def get(self, request, *args):

        wallet_is_con = User.objects.filter(username=request.user).values('wallet_connect')[0]
        btc_wallet = WalletBitcoin.objects.filter(userid=request.user).values()[0]
        bank_wallet = WalletBank.objects.filter(userid=request.user).values()[0]
        form_transfer_btc = TransferBtc()
        form_login_btc = LoginBtc(initial={"wallet": btc_wallet['account'],
                                           "password": btc_wallet['password']})
        # get get_btc_value() esta atrasando o carregamento da pagina
        # value_btc = get_btc_value()
        print(wallet_is_con['wallet_connect'])
        if 'off' in wallet_is_con['wallet_connect']:
            return render(request, self.template_name, {'btc_wallet': btc_wallet,
                                                        'bank_wallet': bank_wallet,
                                                        'wallet_is_con': wallet_is_con['wallet_connect'],
                                                        'form_login_btc': form_login_btc})
        info_wallet = WalletBitcoin.objects.filter(account=wallet_is_con['wallet_connect']).values()

        return render(request, self.template_name, {'info_wallet': info_wallet[0],
                                                    'wallet_is_con': wallet_is_con,
                                                    'form_transfer_btc':form_transfer_btc})

    def post(self, request, *args):
        # print(request.POST)
        print(request.POST)
        wallet_is_con = User.objects.filter(username=request.user).values('wallet_connect')
        if 'off' in wallet_is_con[0]['wallet_connect']:
            print('tem')
        if 'logout_btc' in request.POST:
            User.objects.filter(username=request.user).update(wallet_connect='off')
            return HttpResponseRedirect("/finances/")

        if 'wallet' in request.POST:
            form_login_btc = LoginBtc(request.POST)

            if form_login_btc.is_valid():
                wallet = request.POST['wallet']
                password = request.POST['password']
                # verificar se existe a carteira
                exists = WalletBitcoin.objects.filter(account=wallet).values()
                if len(exists) < 1:
                    msg_erro = 'essa carteira nao existe'
                    return render(request, self.template_name, {'form_login_btc': form_login_btc,
                                                                'msg_erro': msg_erro})
                else:
                    if password == exists[0]['password']:
                        saldo = exists[0]['balance']
                        User.objects.filter(username=request.user).update(wallet_connect=wallet)
                        return HttpResponseRedirect("/finances/")
                    else:
                        msg_erro = 'senha incorreta'
                        return render(request, self.template_name, {'form_login_btc': form_login_btc,
                                                                    'msg_erro': msg_erro})
            else:
                return HttpResponseRedirect(f"/errrrrrrrrrrrrrrro")
