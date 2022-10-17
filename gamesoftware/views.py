from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import Software, TypeSofts



class SoftwareView(TemplateView):
    template_name = "software.html"

    def get(self, request):
        softs = Software.objects.filter(userid=request.user).values()
        typesoft = TypeSofts.objects.filter()
        print('------------------------------------')
        print(typesoft)

        print('------------------------------------')

        return render(request, self.template_name, {'softwares': softs, 'typesofts':typesoft})

