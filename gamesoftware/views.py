from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Software, TypeSofts
from django.http import HttpResponseRedirect
from datetime import timedelta, date, datetime
from controller.models import *



class SoftwareView(TemplateView):
    template_name = "software.html"
   



    def get(self, request):
        softs = Software.objects.filter(userid=request.user).values()
        typesoft = TypeSofts.objects.filter()
        return render(request, self.template_name, {'softwares': softs, 'typesoft':typesoft})

    def post(self, request):
    	ip_connect = User.objects.filter(username=request.user).values('ipconnected')[0]['ipconnected']
    	
    	for valor in request.POST:
            if 'delsoftid=' in valor:
                softid = valor.split('=')[1]
                endtime = datetime.now() + timedelta(seconds=10)
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
	                endtime = datetime.now() + timedelta(seconds=10)
	                Processes.objects.create(userid=request.user,
	                                         action=5,
	                                         timestart=datetime.now(),
	                                         timeend=endtime, softupload=softid, uploadip=ip_connect)
	                return HttpResponseRedirect("/task/")



    	return HttpResponseRedirect("/task/")





