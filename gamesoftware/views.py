from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from datetime import timedelta, datetime
from controller.models import *


class SoftwareView(TemplateView):
    template_name = "software.html"

    def get(self, request, *args):
        softs = Software.objects.filter(userid=request.user).values()
        typesoft = TypeSofts.objects.filter()
        return render(request, self.template_name, {'softwares': softs, 'typesoft': typesoft})

    def post(self, request):
        ip_connect = User.objects.filter(username=request.user).values('ipconnected')[0]['ipconnected']

        for valor in request.POST:
            print(request.POST[valor])
            if 'delsoftid=' in valor:
                softid = valor.split('=')[1]
                endtime = datetime.now() + timedelta(seconds=1)
                Processes.objects.create(userid=request.user,
                                         action=4,
                                         timestart=datetime.now(),
                                         timeend=endtime, softdownload=softid, delmysoft=True)
                return HttpResponseRedirect("/task/")
            if 'uploadsoftid=' in valor:
                ip_connect = User.objects.filter(username=request.user).values('ipconnected')[0]['ipconnected']
                if 'off' in ip_connect:
                    pass
                else:
                    softid = valor.split('=')[1]
                    endtime = datetime.now() + timedelta(seconds=1)
                    Processes.objects.create(userid=request.user,
                                             action=5,
                                             timestart=datetime.now(),
                                             timeend=endtime, softupload=softid, uploadip=ip_connect)
                    return HttpResponseRedirect("/task/")
            if 'runsoft' in request.POST[valor]:
                softid = valor
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=6,
                                                          softrun=softid,
                                                          completed=False,
                                                          ismyserver=True).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=1)
                Processes.objects.create(userid=request.user,
                                         action=6,
                                         timestart=datetime.now(),
                                         timeend=endtime,
                                         softrun=softid,
                                         ismyserver=True)
                return HttpResponseRedirect("/task/")

            if 'stopsoft' in request.POST[valor]:
                softid = valor
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=7,
                                                          softstop=softid,
                                                          completed=False,
                                                          ismyserver=True).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=1)
                Processes.objects.create(userid=request.user,
                                         action=7,
                                         timestart=datetime.now(),
                                         timeend=endtime,
                                         softstop=softid,
                                         ismyserver=True)
                return HttpResponseRedirect("/task/")

            if 'runsoft' in request.POST[valor]:
                softid = valor
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=6,
                                                          softrun=softid, completed=False).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=6,
                                         timestart=datetime.now(),
                                         timeend=endtime,
                                         softrun=softid,
                                         ipvictim=ip_connect,
                                         ismyserver=True)
                return HttpResponseRedirect("/task/")
        return HttpResponseRedirect("/task/")
