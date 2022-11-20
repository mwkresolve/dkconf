from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Hardware, User
from gamefinances.models import WalletBank


class ActionsHardware:
    def __int__(self, request):
        self.request = request

    def get_next_upgrade(self, cpu=0, hdd=0, ram=0):
        next_cpu = cpu + 512
        next_hdd = hdd + 1000
        net_ram = ram + 256
        return {'cpu': next_cpu, 'hdd': next_hdd, 'ram': net_ram, }


class HardwareView(TemplateView, ActionsHardware):
    def __init__(self):
        super().__init__()
        self.template_name = "basehardware.html"

    def get(self, request, *args):
        user_hardware = Hardware.objects.filter(userid=self.request.user).values()
        cpu = user_hardware[0]['cpu']
        next_upgrade_cpu = int(cpu * 2 / 15)
        hdd = user_hardware[0]['hdd']
        next_upgrade_hdd = int(hdd * 2 / 10)
        ram = user_hardware[0]['ram']
        next_upgrade_ram = int(ram * 2 / 4)
        next_upgrade = self.get_next_upgrade(cpu=cpu, hdd=hdd, ram=ram)

        return render(request, self.template_name, {'user_hardware': user_hardware,
                                                    'next_upgrade': next_upgrade,
                                                    'next_upgrade_cpu': next_upgrade_cpu,
                                                    'next_upgrade_hdd': next_upgrade_hdd,
                                                    'next_upgrade_ram': next_upgrade_ram,
                                                    })

    def post(self, request):
        balance = WalletBank.objects.filter(userid=request.user).values('balance')[0]['balance']
        user_hardware = Hardware.objects.filter(userid=self.request.user).values()
        cpu = user_hardware[0]['cpu']
        next_upgrade_cpu = int(cpu * 2 / 15)
        hdd = user_hardware[0]['hdd']
        next_upgrade_hdd = int(hdd * 2 / 10)
        ram = user_hardware[0]['ram']
        next_upgrade_ram = int(ram * 2 / 4)
        next_upgrade = self.get_next_upgrade(cpu=cpu, hdd=hdd, ram=ram)

        print(request.POST)
        if 'upgradecpu' in request.POST:
            value_next_upgrade = int(cpu * 2 / 15)
            if balance < value_next_upgrade :
                msg_erro_cpu = 'SALDO INSUCIFIENTE'
                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'next_upgrade_cpu': next_upgrade_cpu,
                                                            'next_upgrade_hdd': next_upgrade_hdd,
                                                            'next_upgrade_ram': next_upgrade_ram,
                                                            'msg_erro_cpu': msg_erro_cpu})
            else:
                Hardware.objects.filter(userid=request.user).update(cpu=cpu + 512)
                WalletBank.objects.filter(userid=request.user).update(balance=balance - value_next_upgrade)
                msg_ok_cpu =  'Upgrade realizado com sucesso'
                user_hardware = Hardware.objects.filter(userid=self.request.user).values()
                cpu = user_hardware[0]['cpu']
                next_upgrade_cpu = int(cpu * 2 / 15)
                hdd = user_hardware[0]['hdd']
                next_upgrade_hdd = int(hdd * 2 / 10)
                ram = user_hardware[0]['ram']
                next_upgrade_ram = int(ram * 2 / 4)
                next_upgrade = self.get_next_upgrade(cpu=cpu, hdd=hdd, ram=ram)
                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'next_upgrade_cpu': next_upgrade_cpu,
                                                            'next_upgrade_hdd': next_upgrade_hdd,
                                                            'next_upgrade_ram': next_upgrade_ram,
                                                            'msg_ok_cpu': msg_ok_cpu})
        if 'upgradehd' in request.POST:
            print('hdddddddddddddd')
            value_next_upgrade = int(hdd * 2 / 10)
            if balance < value_next_upgrade:
                msg_erro_hd = 'SALDO INSUCIFIENTE'

                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'msg_erro_hd': msg_erro_hd})
            else:
                Hardware.objects.filter(userid=request.user).update(hdd=hdd + 1000)

                WalletBank.objects.filter(userid=request.user).update(balance=balance - value_next_upgrade)
                msg_ok_hdd =  'Upgrade realizado com sucesso'
                user_hardware = Hardware.objects.filter(userid=self.request.user).values()
                cpu = user_hardware[0]['cpu']
                next_upgrade_cpu = int(cpu * 2 / 15)
                hdd = user_hardware[0]['hdd']
                next_upgrade_hdd = int(hdd * 2 / 10)
                ram = user_hardware[0]['ram']
                next_upgrade_ram = int(ram * 2 / 4)
                next_upgrade = self.get_next_upgrade(cpu=cpu, hdd=hdd, ram=ram)
                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'next_upgrade_cpu': next_upgrade_cpu,
                                                            'next_upgrade_hdd': next_upgrade_hdd,
                                                            'next_upgrade_ram': next_upgrade_ram,
                                                            'msg_ok_hdd': msg_ok_hdd})


        if 'upgraderam' in request.POST:
            value_next_upgrade = ram * 2 / 4
            if balance < value_next_upgrade:
                msg_erro_ram = 'SALDO INSUCIFIENTE'

                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'msg_erro_hd': msg_erro_ram})
            else:
                Hardware.objects.filter(userid=request.user).update(ram=ram + 256)

                WalletBank.objects.filter(userid=request.user).update(balance=balance - value_next_upgrade)
                msg_ok_ram =  'Upgrade realizado com sucesso'
                user_hardware = Hardware.objects.filter(userid=self.request.user).values()
                cpu = user_hardware[0]['cpu']
                next_upgrade_cpu = int(cpu * 2 / 15)
                hdd = user_hardware[0]['hdd']
                next_upgrade_hdd = int(hdd * 2 / 10)
                ram = user_hardware[0]['ram']
                next_upgrade_ram = int(ram * 2 / 4)
                next_upgrade = self.get_next_upgrade(cpu=cpu, hdd=hdd, ram=ram)
                return render(request, self.template_name, {'user_hardware': user_hardware,
                                                            'next_upgrade': next_upgrade,
                                                            'next_upgrade_cpu': next_upgrade_cpu,
                                                            'next_upgrade_hdd': next_upgrade_hdd,
                                                            'next_upgrade_ram': next_upgrade_ram,
                                                            'msg_ok_ram': msg_ok_ram})




