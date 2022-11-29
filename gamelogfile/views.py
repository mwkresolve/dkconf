from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Processes, User
from datetime import timedelta, date, datetime
from controller.functionsdb import *


class LogPageView(TemplateView):
    template_name = "log.html"

    def get(self, request, *args):
        my_log = User.objects.filter(username=request.user).values('log')[0]['log']
        return render(request, self.template_name, {'mylog': my_log})

    def post(self, request):
        my_log = User.objects.filter(username=request.user).values('log')[0]['log']
        if request.method == "POST":
            if request.POST["editlog"]:
                editlogactive = len(Processes.objects.filter(userid=request.user,
                                                             action=1,
                                                             completed=False,
                                                             ismyserver=True))
                # usuario só pode ter 1 task ativa para completar
                if editlogactive > 0:
                    # criar msg de aviso no front que ja existe uma tarefa em andamento
                    msg_erro = 'ja existe uma tarefa igual em execução'
                    return render(request, self.template_name, {'mylog': my_log, 'msg_erro': msg_erro})
                else:
                    endtime = datetime.now() + timedelta(seconds=3)
                    current_log = request.POST.get('logarea')
                    Processes.objects.create(userid=request.user,
                                             action=1,
                                             timestart=datetime.now(),
                                             timeend=endtime, logedit=current_log,
                                             ismyserver=True)
                    return HttpResponseRedirect("/task/")
