from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Processes, User
from datetime import timedelta, date, datetime
from controller.functionsdb import *
from .models import *


class FinancesView(TemplateView):
    template_name = "finances.html"

    def get(self, request):
        btc_wallet = WalletBitcoin.objects.filter(userid=request.user).values()[0]
        return render(request, self.template_name, {'btc_wallet': btc_wallet})

    def post(self, request):
        if request.method == "POST":
            if request.POST["editlog"]:
                editlogactive = len(Processes.objects.filter(userid=request.user, action=1, completed=False))
                # usuario só pode ter 1 task ativa para completar
                if editlogactive > 0:
                    # criar msg de aviso no front que ja existe uma tarefa em andamento
                    return HttpResponseRedirect("/log/")
                else:
                    endtime = datetime.now() + timedelta(seconds=3)
                    current_log = request.POST.get('logarea')
                    Processes.objects.create(userid=request.user,
                                             action=1,
                                             timestart=datetime.now(),
                                             timeend=endtime, logedit=current_log)
                    return HttpResponseRedirect("/task/")
