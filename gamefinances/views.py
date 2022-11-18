from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import TemplateView


class ActionFinancesBtc:
    def __int__(self, request):
        self.request = request

    def get_is_conn_btc(self):
        """
        :return: off or wallet btc connected
        """
        return User.objects.filter(username=self.request.user).values('wallet_connect')[0]['wallet_connect']

    # account_bank_connect
    def get_is_conn_bank(self):
        """
        :return: off or wallet btc connected
        """
        return User.objects.filter(username=self.request.user).values('account_bank_connect')[0]['account_bank_connect']

    def get_info_btc_user(self):
        """
        :return: infos wallet btc user
        """
        return WalletBitcoin.objects.filter(userid=self.request.user).values()[0]

    def get_info_bank_user(self):
        """
        :return: infos wallet btc user
        """
        return WalletBank.objects.filter(userid=self.request.user).values()[0]

    def transfer_from_to(self, fromwallet, towallet, value):
        wallet_sender = WalletBitcoin.objects.filter(account=fromwallet).values('balance')[0]['balance']
        wallet_receiver = WalletBitcoin.objects.filter(account=towallet).values('balance')[0]['balance']
        WalletBitcoin.objects.filter(account=fromwallet).update(balance=wallet_sender - value)
        WalletBitcoin.objects.filter(account=towallet).update(balance=wallet_receiver + value)
    def transfer_from_to_bank(self, frombank, tobank, value):
        wallet_sender = WalletBank.objects.filter(account=frombank).values('balance')[0]['balance']
        wallet_receiver = WalletBank.objects.filter(account=tobank).values('balance')[0]['balance']
        WalletBank.objects.filter(account=frombank).update(balance=wallet_sender - value)
        WalletBank.objects.filter(account=tobank).update(balance=wallet_receiver + value)


class FinancesView(TemplateView, ActionFinancesBtc):
    def __init__(self):
        super().__init__()
        self.template_name = "finances.html"
        self.form_transfer_btc = TransferBtc()
        self.form_login_btc = LoginBtc()
        self.form_login_bank = LoginBank()
        self.form_transfer_bank = TransferBank()
        self.data = dict()
        self.info_wallet = ''
        self.info_bank = ''
        self.msg_erro_btc = ''
        self.msg_erro_bank = ''

    def get(self, request, *args):

        if 'off' in self.get_is_conn_btc():

            self.form_login_btc = LoginBtc(initial={"wallet": self.get_info_btc_user()['account'],
                                                    "password": self.get_info_btc_user()['password']})
        else:
            self.info_wallet = WalletBitcoin.objects.filter(account=self.get_is_conn_btc()).values()
        if 'off' in self.get_is_conn_bank():

            self.form_login_bank = LoginBank(initial={"account": self.get_info_bank_user()['account'],
                                                      "password": self.get_info_bank_user()['password']})

        else:
            self.info_bank = WalletBank.objects.filter(account=self.get_is_conn_bank()).values()

        return render(request, self.template_name, {'form_login_btc': self.form_login_btc,
                                                    'form_login_bank': self.form_login_bank,
                                                    'info_wallet': self.get_info_btc_user(),
                                                    'wallet_is_con': self.get_is_conn_btc(),
                                                    'wallet_is_con_bank': self.get_is_conn_bank(),
                                                    'bank_wallet': self.get_info_bank_user(),
                                                    'form_transfer_btc': self.form_transfer_btc,
                                                    'form_transfer_bank': self.form_transfer_bank})

    def post(self, request):
        print(request.POST)
        self.form_login_bank = LoginBank(initial={"account": self.get_info_bank_user()['account'],
                                                  "password": self.get_info_bank_user()['password']})

        bank_wallet = WalletBank.objects.filter(userid=request.user).values()[0]


        if 'logout_bank' in request.POST:
            if 'off' in self.get_is_conn_bank():
                return HttpResponseRedirect("/tenta de novo hackzin/")
            User.objects.filter(username=request.user).update(account_bank_connect='off')
            return HttpResponseRedirect("/finances/")

        if 'transf_to_bank' in request.POST:
            form_transf_bank = TransferBank(request.POST)
            if form_transf_bank.is_valid():
                bank_connect = self.get_is_conn_bank()
                transf_to = request.POST['transf_to_bank']
                value_transf = float(request.POST['value'])
                exists = WalletBank.objects.filter(account=transf_to).values()
                info_wallet = WalletBank.objects.filter(account=self.get_is_conn_btc()).values()
                saldo_bank = float(
                    WalletBank.objects.filter(account=bank_connect).values('balance')[0]['balance'])


                if len(exists) < 1:
                    self.msg_erro_bank = f'a carteira {transf_to} não existe'
                    return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank
                                                                })
                if transf_to == bank_connect:
                    self.msg_erro_bank = f'você nao pode transferir para a mesma conta'
                    return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank
                                                                })
                if value_transf > saldo_bank:
                    self.msg_erro_bank = f'Seu saldo é menor que {value_transf}  '
                    return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank
                                                                })
                self.transfer_from_to_bank(frombank=bank_connect,
                                      tobank=transf_to,
                                      value=value_transf)
                # transformar isso em msg verde separar as msg erro de msg sucess
                self.msg_erro_bank = f'Dinheiro transferido  '
                return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                            'form_login_btc': self.form_login_btc,
                                                            'form_login_bank': self.form_login_bank,
                                                            'info_wallet': self.get_info_btc_user(),
                                                            'wallet_is_con': self.get_is_conn_btc(),
                                                            'wallet_is_con_bank': self.get_is_conn_bank(),
                                                            'bank_wallet': bank_wallet,
                                                            'form_transfer_btc': self.form_transfer_btc,
                                                            'form_transfer_bank': self.form_transfer_bank
                                                            })


        if 'account' in request.POST:
            self.form_login_btc = LoginBtc(initial={"wallet": self.get_info_btc_user()['account'],
                                                    "password": self.get_info_btc_user()['password']})
            self.form_login_bank = LoginBank(initial={"account": self.get_info_bank_user()['account'],
                                                      "password": self.get_info_bank_user()['password']})
            form_login_bank = LoginBank(request.POST)
            if form_login_bank.is_valid():

                info_wallet = WalletBank.objects.filter(account=self.get_is_conn_bank()).values()
                account = request.POST['account']
                password = request.POST['password']
                # verificar se existe a carteira
                exists = WalletBank.objects.filter(account=account).values()
                if len(exists) < 1:
                    self.msg_erro_bank = 'essa conta nao existe'
                    return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank
                                                                })
                else:
                    if password == exists[0]['password']:
                        User.objects.filter(username=request.user).update(account_bank_connect=account)
                        return HttpResponseRedirect("/finances/")
                    else:
                        self.msg_erro_bank = 'senha incorreta'
                        return render(request, self.template_name, {'msg_erro_bank': self.msg_erro_bank,
                                                                    'form_login_btc': self.form_login_btc,
                                                                    'form_login_bank': self.form_login_bank,
                                                                    'info_wallet': self.get_info_btc_user(),
                                                                    'wallet_is_con': self.get_is_conn_btc(),
                                                                    'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                    'bank_wallet': bank_wallet,
                                                                    'form_transfer_btc': self.form_transfer_btc,
                                                                    'form_transfer_bank': self.form_transfer_bank
                                                                    })

            else:
                return HttpResponseRedirect(f"/errrrrrrrrrrrrrrro")

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
                saldo_wallet = float(
                    WalletBitcoin.objects.filter(account=wallet_connect).values('balance')[0]['balance'])
                exists = WalletBitcoin.objects.filter(account=transf_to).values()
                info_wallet = WalletBitcoin.objects.filter(account=self.get_is_conn_btc()).values()
                # se nao existir a carteira retorna erro
                if len(exists) < 1:
                    self.msg_erro_btc = f'a carteira {transf_to} não existe'
                    return render(request, self.template_name, {'msg_erro_btc': self.msg_erro_btc,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank,
                                                                })

                if transf_to == wallet_connect:
                    self.msg_erro_btc = f'você nao pode transferir para a mesma conta'
                    return render(request, self.template_name, {'msg_erro_btc': self.msg_erro_btc,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                'form_transfer_bank': self.form_transfer_bank,
                                                                })
                if value_transf > saldo_wallet:
                    self.msg_erro_btc = f'você não possui saldo para transferir {value_transf} bitcoins'

                    return render(request, self.template_name, {'msg_erro_btc': self.msg_erro_btc,
                                                                'form_login_btc': self.form_login_btc,
                                                                'form_login_bank': self.form_login_bank,
                                                                'info_wallet': self.get_info_btc_user(),
                                                                'wallet_is_con': self.get_is_conn_btc(),
                                                                'wallet_is_con_bank': self.get_is_conn_bank(),
                                                                'bank_wallet': bank_wallet,
                                                                'form_transfer_btc': self.form_transfer_btc,
                                                                })
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
            self.form_login_btc = LoginBtc(initial={"wallet": self.get_info_btc_user()['account'],
                                                    "password": self.get_info_btc_user()['password']})
            self.form_login_bank = LoginBank(initial={"account": self.get_info_bank_user()['account'],
                                                      "password": self.get_info_bank_user()['password']})
            form_login_btc = LoginBtc(request.POST)
            if form_login_btc.is_valid():
                info_wallet = WalletBitcoin.objects.filter(account=self.get_is_conn_btc()).values()
                wallet = request.POST['wallet']
                password = request.POST['password']
                # verificar se existe a carteira
                exists = WalletBitcoin.objects.filter(account=wallet).values()
                if len(exists) < 1:
                    self.msg_erro_btc = 'essa carteira nao existe'
                    return render(request, self.template_name, {
                        'bank_wallet': bank_wallet,
                        'wallet_is_con': self.get_is_conn_btc(),
                        'msg_erro_btc': self.msg_erro_btc,
                        'form_login_btc': self.form_login_btc,
                        'wallet_is_con_bank': self.get_is_conn_bank(),
                        'form_login_bank': self.form_login_bank,
                    })
                else:
                    if password == exists[0]['password']:
                        User.objects.filter(username=request.user).update(wallet_connect=wallet)
                        return HttpResponseRedirect("/finances/")
                    else:
                        self.msg_erro_btc = 'senha incorreta'
                        return render(request, self.template_name, {
                            'bank_wallet': bank_wallet,
                            'wallet_is_con': self.get_is_conn_btc(),
                            'msg_erro_btc': self.msg_erro_btc,
                            'form_login_btc': self.form_login_btc,
                            'wallet_is_con_bank': self.get_is_conn_bank(),
                            'form_login_bank': self.form_login_bank,
                        })

            else:
                return HttpResponseRedirect(f"/errrrrrrrrrrrrrrro")
