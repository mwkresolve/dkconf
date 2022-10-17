from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import User, Hardware, TypeSofts, Software, UserStats,  HistUsersCurrent
from my_tools.functions import *
from .functionsdb import *
import json

def HomePageView(request):
    try:
        if not request.user.stats_game:
            create_user_game(request.user)
            return render(request, "newplayer.html")
    except:
        return render(request, "home.html")
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
            return render(request, 'controller.html')
        return render(request, 'home.html')
