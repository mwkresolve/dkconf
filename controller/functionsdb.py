from .models import *
from gamefinances.models import *
from my_tools.functions import *
import names
import random
import math
from datetime import datetime
from django.db.models import Q


def disconnect_ip_victim(user):
    User.objects.filter(username=user).update(ipconnected='off')
def connect_ip_victim(user, ip):
    User.objects.filter(username=user).update(ipconnected=ip)
def create_user_game(user):
    """
    por enquanto isto está sendo usado quando o usuario loga pela primeira vez no jogo
    para popular as infos necessarias para jogar, quando for pra produção isso deve ser
    movido para quando o jogador confirmar a conta no e-mail ja criar as stats
    """
    try:

        Hardware.objects.create(userid=user)
        HistUsersCurrent.objects.create(userid=user)
        User.objects.update(stats_game=True)
        LastIp.objects.create(user=user)
        WalletBitcoin.objects.create(userid=user,
                                     account=generate_account(),
                                     password=generate_pw(),
                                     )
        WalletBank.objects.create(userid=user,
                                  account=generate_num_account(),
                                  password=pwd_generator(),
                                  )
        return True
    except:
        return False


def npc_basic_config():
    """ existem os servidores de enigma
        esses serão servidores mais simples e mais fracos
        so pra fazer volume msm
        por hora ta simulando outros players
     """
    try:
        for c in range(100):
            name = f'{names.get_last_name()}_{names.get_first_name()}'
            user_1 = User.objects.create_user(f'{name}', f'{name}@chase.com', 'chevyspgererassword', isnpc=1)
            create_user_game(user_1)
            update_reputation(user_1, random.randint(100, 10000))
    except:
        pass


def creategame():
    Softs_Types = {
        '1': '.Cracker',
        '2': '.Hasher',
        '3': '.PortScan',
        '4': '.Firewall',
        '5': '.Hidder',
        '6': '.Seeker',
        '7': '.Anti-Virus',
        '8': '.Spam',
        '9': '.Warez',
        '10': '.DDoS',
        '11': '.Collector',
        '12': '.Breaker',
        '13': '.FTPExploit',
        '14': '.SSHExploit',
        '15': '.Nmap',
        '16': '.Analyzer',
        '17': '.Torrent',
        '20': '.Miner',
        '21': '.enigma',
    }
    for soft in Softs_Types:
        TypeSofts.objects.create(type=Softs_Types[soft])


def create_npc_game():
    npc_data = open('my_tools/info_bots.json').read()
    npcList = json.loads(npc_data)

    for bot in npcList:
        name = npcList[bot]['nome']
        gameip = npcList[bot]['ip']
        # create usernpc
        if 'create' in gameip:
            gameip = ip_generator()
        User.objects.create(username=name,
                            isnpc=True,
                            gameip=gameip,
                            gamepass=pwd_generator(),
                            istrail=True)

    create_hardware_npc()
    create_softs_npc()
    npc_basic_config()
    create_enigmas()


def create_hardware_npc():
    npc_data = open('my_tools/info_bots.json').read()
    npcList = json.loads(npc_data)
    for bot in npcList:
        user = User.objects.get(username=npcList[bot]['nome'])
        cpu = npcList[bot]['cpu']
        hdd = npcList[bot]['hdd']
        ram = npcList[bot]['ram']
        Hardware.objects.create(userid=user, cpu=cpu, hdd=hdd, ram=ram)


def reset_softs_npc():
    # need this run every 30 minutes in cron job
    npc_data = open('my_tools/info_bots.json').read()
    npcList = json.loads(npc_data)
    for bot in npcList:
        user = User.objects.get(username=npcList[bot]['nome'])
        # deletar todos os softs dos bot menos .enigma
        Software.objects.filter(~Q(softtype='19'), userid=user).delete()
    create_softs_npc()



def create_enigmas():
    ips_trilha = User.objects.filter(istrail=True).values()
    questions = open('my_tools/enigma.json').read()
    questions_list = json.loads(questions)
    for c in range(1, len(questions_list) + 1):
        pergunta = questions_list[f'enigma{c}']['pergunta']
        resposta = questions_list[f'enigma{c}']['resposta']
        bot_trail = User.objects.get(username=ips_trilha[c - 1]['username'])
        # bot_trail = ips_trilha[c]['username']
        current_ip = ips_trilha[c - 1]['gameip']

        next_ip = ips_trilha[c]['gameip']
        typesoft = TypeSofts.objects.get(type='.enigma')

        Enigma.objects.create(ip_trail=bot_trail,
                              pergunta=pergunta,
                              resposta=resposta,
                              next_ip=next_ip,
                              current_ip=current_ip)

        a = Software.objects.create(userid=bot_trail, softname='secret',
                                    softversion=0,
                                    softsize=0,
                                    softram=0,
                                    softtype=typesoft, softhidden=0, softhiddenwith=0)


def create_softs_npc():
    npc_data = open('my_tools/info_bots.json').read()
    npcList = json.loads(npc_data)
    softsize = 100
    softram = 25
    for bot in npcList:
        user = User.objects.get(username=npcList[bot]['nome'])
        for softs in npcList[bot]['softs']['soft'].values():
            typesoft = TypeSofts.objects.get(type=softs['type'])
            version = softs['version']
            softsize = 25
            softram = 10
            Software.objects.create(userid=user, softname='s1mple',
                                    softversion=version,
                                    softsize=softsize,
                                    softram=softram,
                                    softtype=typesoft, softhidden=0, softhiddenwith=0)

        softsize += 100
        softram += 25



def update_reputation(user, sumreputation):
    old_rep = HistUsersCurrent.objects.filter(userid=user).values('reputation')[0]['reputation']
    new_rep = old_rep + sumreputation
    HistUsersCurrent.objects.filter(userid=user).update(reputation=new_rep)


def disconnect_ip_victim(user):
    User.objects.filter(username=user).update(ipconnected='off')
    update_reputation(user, 1)


def connect_ip_victim(user, ip):
    User.objects.filter(username=user).update(ipconnected=ip)
    update_reputation(user, 1)


def edit_my_log(user, logedit, oldlog=True):
    old_log_user = ''
    if oldlog:
        old_log_user = User.objects.filter(username=user).values('log')[0]['log'].strip()

    User.objects.filter(username=user).update(log=f'{old_log_user}\n{logedit} at {get_current_time()}')
    update_reputation(user, 10)


def edit_log_victim(gameip_victim, logedit):
    User.objects.filter(gameip=gameip_victim).update(log=logedit)


def edit_log_usr_and_victim(user, gameip_victim, logedit):
    old_log_victim = User.objects.filter(gameip=gameip_victim).values('log')[0]['log']
    edit_my_log(user, f'\n{logedit}')
    edit_log_victim(gameip_victim, old_log_victim + f'\n{logedit} at {get_current_time()}')


def get_current_time():
    return datetime.now().strftime('%H:%M:%S')
