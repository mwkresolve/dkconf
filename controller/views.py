from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import User, Hardware, TypeSofts, Software
from my_tools.functions import *
from .functionsdb import *
import json


def HomePageView(request):
        first_acess = User.objects.filter(stats_game=False)
        if first_acess:
            create_user_game(request.user)
            return render(request, "newplayer.html")
        return render(request, "home.html")

class Controller(TemplateView):
    template_name = 'controller.html'
    npc_data = open('my_tools/info_bots.json').read()
    npcList = json.loads(npc_data)

    def get(self, request):
        if request.user.is_staff == 1:
            if request.GET.get('createnpc'):
                create_npc_game()
            if request.GET.get('creategame'):
                creategame()
            if request.GET.get('resetsoftsnpc'):
                reset_softs_npc()

            return render(request, 'controller.html')
        return render(request, 'home.html')
