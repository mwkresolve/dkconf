import re
from datetime import timedelta, date, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView , CreateView
from controller.models import User, Processes, Software, TypeSofts, HackedDatabase, LastIp
from controller.functionsdb import *
from django.contrib.auth.decorators import login_required
from .forms import *


def GenerateIpUrl():
    get_ips = User.objects.values('gameip')
    all_ips_game = list()
    for ip in get_ips.iterator():
        all_ips_game.append(ip['gameip'])
    return all_ips_game


@login_required
def disconnectuser(request):
    info_user = User.objects.filter(username=request.user).values()
    ip_connect = info_user[0]['ipconnected']
    if ip_connect == 'off':
        return HttpResponse("continue tentando!")
    else:
        disconnect_ip_victim(request.user)
        return HttpResponseRedirect("/netip=0.0.0.0")


class ConnectIpView(CreateView):
    template_name = "internet_connect_ip_ok.html.html"

    def get(self, request, *args):
        info_user = User.objects.filter(username=request.user).values()
        ip_connect = info_user[0]['ipconnected']
        victim = User.objects.filter(gameip=ip_connect).values('log', 'username', 'id')
        softs_victim = Software.objects.filter(userid=victim[0]['id']).values()
        return render(request, "internet_connect_ip_ok.html", {'softs_victim': softs_victim})
    def post(self, request, *args):

        info_user = User.objects.filter(username=request.user).values()
        ip_connect = info_user[0]['ipconnected']
        for info in request.POST:
            print(request.POST)
            soft_id = info
            if 'Resolver' in request.POST[info]:
                return HttpResponseRedirect(f"/netip={ip_connect}isconnected=ok=enigma")
            if 'logout' in request.POST[info]:
                disconnectuser(request)
                return HttpResponseRedirect(f"/netip={ip_connect}")
            if 'download' in request.POST[info]:
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                         action=3,
                                                          softdownload=soft_id, completed=False).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=3,
                                         timestart=datetime.now(),
                                         timeend=endtime, softdownload=soft_id)
                return HttpResponseRedirect("/task/")
            if 'delete' in request.POST[info]:
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=4,
                                                          softdel=soft_id, completed=False).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")

                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=4,
                                         timestart=datetime.now(),
                                         timeend=endtime, softdel=soft_id)
                return HttpResponseRedirect("/task/")
            if 'runsoft' in request.POST[info]:
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=6,
                                                          softrun=soft_id, completed=False).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=6,
                                         timestart=datetime.now(),
                                         timeend=endtime, softrun=soft_id, ipvictim=ip_connect)
                return HttpResponseRedirect("/task/")
            if 'stopsoft' in request.POST[info]:
                chk_exists = len(Processes.objects.filter(userid=request.user,
                                                          action=7,
                                                          softstop=soft_id, completed=False).values()) >= 1

                if chk_exists:
                    return HttpResponse("ja existe")
                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=7,
                                         timestart=datetime.now(),
                                         timeend=endtime, softstop=soft_id, ipvictim=ip_connect)
                return HttpResponseRedirect("/task/")







@login_required
def hackip(request, msgbroke, ip_victim):
    info_victim = User.objects.filter(gameip=ip_victim).values('isnpc', 'username', 'gamepass')

    for info in info_victim:
        if info['isnpc']:
            text_npc = f'Olá invasor, meu nome é {info["username"]}.</br> quem sabe eu possa te ajudar se você me responder uma pergunta ' \
                       f'\nMas espera ai, sera que você consegue me invadir?'
            """
            return render(request, "internethack.html", {'ip_victim': ip_victim,
                                                         'text_npc': text_npc, 
                                                         'msgbroke':msgbroke})

            """
            return HttpResponseRedirect(f"/netip={ip_victim}", {'ip_victim': ip_victim,
                                                                'text_npc': text_npc,
                                                                'msgbroke': msgbroke})

        else:
            # return render(request, "internethack.html", {'msgbroke':msgbroke})
            return HttpResponseRedirect(f"/netip={ip_victim}", {'ip_victim': ip_victim, 'msgbroke': msgbroke})



class NetView(CreateView):
    template_name = "internetip.html"
    regex_ip = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
    form_find_ip = FindIp()
    form_get_pw = VictimIp()
    def get(self, request, *args):
        info_user = User.objects.filter(username=request.user).values()
        ip_victim = re.findall(self.regex_ip, request.get_full_path())[0]
        form_find_ip = FindIp(initial={"ip": ip_victim})
        form_login_victim = VictimIp(initial={"login": "root"})
        ip_connect = info_user[0]['ipconnected']
        last_ip = LastIp.objects.filter(user=request.user).values()
        LastIp.objects.filter(user=request.user).update(ip=ip_victim)
        ishacked = len(HackedDatabase.objects.filter(userid=request.user, iphacked=ip_victim).values()) >= 1
        # verificar se esta conectado em algum ip, se sim redireciona pro ip
        if ip_connect != 'off':
            return HttpResponseRedirect(f"/netip={ip_connect}isconnected=ok")
        # verificando se o ip existe no jogo
        if ip_victim not in GenerateIpUrl():
            msgerro = f'O IP {ip_victim} não existe'
            return render(request, self.template_name, {'msgerro': msgerro,  'form_find_ip': form_find_ip, 'form_login_victim':form_login_victim})
        # se existir joga pra tela de login
        else:
            # !!!!!!!!!!! criar funcao para mostrar o texto dos servidores bots
            # condição pra mostrar a senha no form, nao decidi se basta a senha ser igual ou root tbm tem
            if ishacked or ip_victim == '0.0.0.0':
                pw = User.objects.filter(gameip=ip_victim).values('gamepass')[0]['gamepass']
                form_login_victim = VictimIp(initial={"login": "root", "pw": pw})
                return render(request, 'internethack.html',
                              {'form_find_ip': form_find_ip, 'form_login_victim': form_login_victim,
                               'ishacked': ishacked})

            #
            return render(request, 'internethack.html',
                          {'form_find_ip': form_find_ip, 'form_login_victim': form_login_victim, 'ishacked': ishacked})

    def post(self, request, *args):

        form_get_pw = VictimIp()
        form_login_victim = VictimIp(initial={"login": "root"})
        ip_victim = re.findall(self.regex_ip, request.get_full_path())[0]
        if ip_victim == User.objects.filter(username=request.user).values('gameip')[0]['gameip']:
            return HttpResponse('nao pode se hackear')
        if 'ip' in request.POST:
            form_find_ip = FindIp(request.POST)
            if form_find_ip.is_valid():
                is_ip = re.findall(self.regex_ip, request.POST['ip'])
                if not is_ip:
                    msgerro = f'Isso {request.POST["ip"]} não é um endereço de ip valido'
                    return render(request, self.template_name, {'msgerro': msgerro,
                                                               'form_find_ip': form_find_ip, 'form_get_pw':form_get_pw})
                return HttpResponseRedirect(f"/netip={request.POST['ip']}")
            else:
                return HttpResponseRedirect(f"/errrrrrrrrrrrrrrro")
        if 'pw' in request.POST:
            form_get_pw = VictimIp(request.POST)
            if form_get_pw.is_valid():
                pw_try = form_get_pw['pw'].value()
                pw_victim = User.objects.filter(gameip=ip_victim).values('gamepass')[0]['gamepass']

                if pw_try == pw_victim:
                    print('entrousssssssssssssssssssssss')
                    connect_ip_victim(request.user, ip_victim)
                    return HttpResponseRedirect(f"/netip={ip_victim}isconnected=ok")
                # finalizar quando a senha esta errada pra nao renderizar a pw
                # se o ip nao estiver no banco de dados
                msgbroke = 'senha incorreta'
                form_find_ip = FindIp(initial={"ip": ip_victim})
                ishacked = len(HackedDatabase.objects.filter(userid=request.user, iphacked=ip_victim).values()) >= 1
                if ishacked: # if not  glitch pra descobrir senha do servidor
                    form_login_victim = VictimIp(initial={"login": "root", "pw": pw_victim})
                return render(request, 'internethack.html', {'msgbroke': msgbroke,
                                                             'form_find_ip': form_find_ip,
                                                             'form_login_victim': form_login_victim})
        if 'tryhack' in request.POST:
            softs_user = Software.objects.filter(userid=request.user, softtype_id=1).values()
            # caso entre na pagina do proprio ip
            if ip_victim == User.objects.filter(username=request.user).values('gameip')[0]['gameip']:
                msgerro = 'você não pode invadir o próprio servidor'
                return render(request, 'internethack.html', {'msgerro': msgerro,
                                                             'form_find_ip': self.form_find_ip,
                                                             'form_login_victim': form_login_victim})

            if not softs_user:
                # pend avisar que ta sem cracker ativo pra essa ação
                msgerro = 'você precisa do software cracker para executar essa ação'
                return render(request, 'internethack.html', {'msgerro': msgerro,
                                                             'form_find_ip': self.form_find_ip,
                                                             'form_login_victim': form_login_victim})

            else:
                chk_exists = len(Processes.objects.filter(action=2, userid=request.user, iptryhack=ip_victim, completed=False).values()) >= 1
                # nao criar tarefa identica
                if chk_exists:
                    msgbroke = 'já existe uma tarefa igual em execução'
                    return render(request, 'internethack.html', {'msgbroke': msgbroke,
                                                                 'form_find_ip': self.form_find_ip,
                                                                 'form_login_victim': form_login_victim})
                endtime = datetime.now() + timedelta(seconds=10)
                Processes.objects.create(userid=request.user,
                                         action=2,
                                         timestart=datetime.now(),
                                         timeend=endtime, iptryhack=ip_victim)
                return HttpResponseRedirect("/task/")
        else:
            print('errro')
            return HttpResponse('keeptrying')


@login_required
def InternetView(request):
    last_ip = LastIp.objects.filter(user=request.user).values()
    if len(last_ip) < 1:
        last_ip = '0.0.0.0'
        return HttpResponseRedirect(f"/netip={last_ip}")
    return HttpResponseRedirect(f"/netip={last_ip[0]['ip']}")


def EnigmaView(request):
    info_user = User.objects.filter(username=request.user).values()
    ip_connected = info_user[0]['ipconnected']
    get_ip_trail = User.objects.filter(gameip=ip_connected).values()
    current_enigma = Enigma.objects.filter(ip_trail_id=get_ip_trail[0]['id']).values()
    pergunta = ''
    resposta = ''
    a = enigma_solved.objects.filter(user=request.user, enigma_ip=ip_connected)
    issolved = a.values()
    for quest in current_enigma:
        if quest['current_ip'] == ip_connected:
            pergunta = quest['pergunta']
            resposta = quest['resposta'].strip()
    try:
        verify_solved = issolved[0]['solved']
        next_ip = current_enigma[0]['next_ip']
    except:
        a = enigma_solved.objects.filter(user=request.user, enigma_ip=ip_connected)
        current_enigma = Enigma.objects.filter(ip_trail_id=get_ip_trail[0]['id']).values()
        a.create(user=request.user, enigma_ip=ip_connected)
        issolved = a.values()
        verify_solved = issolved[0]['solved']
        next_ip = current_enigma[0]['next_ip']
    if request.method == "POST":
        if request.POST.get('action') == 'resp':
            resp_user = request.POST.get('resp').strip()
            if resposta == resp_user:
                enigma_solved.objects.filter(user_id=request.user, enigma_ip=ip_connected).update(solved=True)
                return HttpResponseRedirect(f"/netip={ip_connected}isconnected=ok=enigma")
    return render(request, "enigma.html", {'pergunta': pergunta, 'verify_solved': verify_solved, 'next_ip': next_ip})
