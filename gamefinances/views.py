from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import TemplateView


class ActionFinancesBtc:
    def __int__(self, request):
        self.request = request
        self.form_transfer_btc = TransferBtc()

    def get_is_conn_btc(self):
        """
        :return: off or wallet btc connected
        """
        return User.objects.filter(username=self.request.user).values('wallet_connect')[0]['wallet_connect']

    def get_info_btc_user(self):
        """
        :return: infos wallet btc user
        """
        return WalletBitcoin.objects.filter(userid=self.request.user).values()[0]

    def transfer_from_to(self, fromwallet, towallet, value):
        wallet_sender = WalletBitcoin.objects.filter(account=fromwallet).values('balance')[0]['balance']
        wallet_receiver = WalletBitcoin.objects.filter(account=towallet).values('balance')[0]['balance']
        WalletBitcoin.objects.filter(account=fromwallet).update(balance=wallet_sender - value)
        WalletBitcoin.objects.filter(account=towallet).update(balance=wallet_receiver + value)


class FinancesView(TemplateView, ActionFinancesBtc):
    def __init__(self):
        super().__init__()
        self.template_name = "finances.html"
        self.form_transfer_btc = TransferBtc()

    def get(self, request, *args):
        bank_wallet = WalletBank.objects.filter(userid=request.user).values()[0]
        form_login_btc = LoginBtc(initial={"wallet": self.get_info_btc_user()['account'],
                                           "password": self.get_info_btc_user()['password']})
        if 'off' in self.get_is_conn_btc():
            return render(request, self.template_name, {'btc_wallet': self.get_info_btc_user(),
                                                        'bank_wallet': bank_wallet,
                                                        'wallet_is_con': self.get_is_conn_btc(),
                                                        'form_login_btc': form_login_btc})
        info_wallet = WalletBitcoin.objects.filter(account=self.get_is_conn_btc()).values()
        return render(request, self.template_name, {'info_wallet': info_wallet[0],
                                                    'bank_wallet': bank_wallet,
                                                    'wallet_is_con': self.get_is_conn_btc(),
                                                    'form_transfer_btc': self.form_transfer_btc})

    def post(self, request):
        print(request.POST)
        bank_wallet = WalletBank.objects.filter(userid=request.user).values()[0]
        if 'logout_btc' in request.POST:
            if 'off' in self.get_is_conn_btc():
                return HttpResponseRedirect("/tenta de novo hackzin/")
            User.objects.filter(username=request.user).update(wallet_connect='off')
            return HttpResponseRedirect("/finances/")
        if 'transf_to_wallet' in request.POST:
            form_transf = TransferBtc(request.POST)
            if form_transf.is_valid():
                wallet_connect = self.get_is_conn_btc()
                transf_to = request.POST['transf_to_wallet']
                value_transf = float(request.POST['value'])
                saldo_wallet = float(WalletBitcoin.objects.filter(account=wallet_connect).values('balance')[0]['balance'])
                exists = WalletBitcoin.objects.filter(account=transf_to).values()
                info_wallet = WalletBitcoin.objects.filter(account=self.get_is_conn_btc()).values()
                # se nao existir a carteira retorna erro
                if len(exists) < 1:
                    msg_erro = f'a carteira {transf_to} não existe'

                    return render(request, self.template_name, {'msg_erro': msg_erro,
                                                                'info_wallet': info_wallet[0],
                                                                'bank_wallet': bank_wallet,
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'form_transfer_btc': self.form_transfer_btc})

                if transf_to == wallet_connect:
                    msg_erro = f'você nao pode transferir para a mesma conta'

                    return render(request, self.template_name, {'msg_erro': msg_erro,
                                                                'info_wallet': info_wallet[0],
                                                                'bank_wallet': bank_wallet,
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'form_transfer_btc': self.form_transfer_btc})
                if value_transf > saldo_wallet:

                    msg_erro = f'você não possui saldo para transferir {value_transf} bitcoins'

                    return render(request, self.template_name, {'msg_erro': msg_erro,
                                                                'info_wallet': info_wallet[0],
                                                                'bank_wallet': bank_wallet,
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'form_transfer_btc': self.form_transfer_btc})

                self.transfer_from_to(fromwallet=wallet_connect,
                                      towallet=transf_to,
                                      value=value_transf)
                msg_erro = 'dinheiro transferido'
                return render(request, self.template_name, {'msg_erro': msg_erro,
                                                            'info_wallet': info_wallet[0],
                                                            'bank_wallet': bank_wallet,
                                                            'wallet_is_con': self.get_is_conn_btc(),
                                                            'form_transfer_btc': self.form_transfer_btc})
        if 'wallet' in request.POST:
            form_login_btc = LoginBtc(request.POST)
            if form_login_btc.is_valid():
                wallet = request.POST['wallet']
                password = request.POST['password']
                # verificar se existe a carteira
                exists = WalletBitcoin.objects.filter(account=wallet).values()
                if len(exists) < 1:
                    msg_erro = 'essa carteira nao existe'
                    return render(request, self.template_name, {
                        'bank_wallet': bank_wallet,
                        'wallet_is_con': self.get_is_conn_btc(),
                        'msg_erro': msg_erro,
                        'form_login_btc': self.form_transfer_btc
                    })
                else:
                    if password == exists[0]['password']:
                        User.objects.filter(username=request.user).update(wallet_connect=wallet)
                        return HttpResponseRedirect("/finances/")
                    else:
                        msg_erro = 'senha incorreta'
                        return render(request, self.template_name, {
                            'bank_wallet': bank_wallet,
                            'wallet_is_con': self.get_is_conn_btc(),
                            'msg_erro': msg_erro,
                            'form_login_btc': form_login_btc
                        })

            else:
                return HttpResponseRedirect(f"/errrrrrrrrrrrrrrro")
