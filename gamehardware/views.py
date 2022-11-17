from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Hardware

class HardwareView(TemplateView):
    template_name = "basehardware.html"

    def get(self, request, *args):
        user_hardware = Hardware.objects.filter(userid=request.user).values()
        return render(request, self.template_name, {'user_hardware': user_hardware})
    def post(self, request, *args):
        pass
