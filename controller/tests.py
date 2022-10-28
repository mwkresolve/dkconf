
from .models import *
from .functionsdb import *
import names
import random
import unittest

class CaseCreateEnigma(unittest.TestCase):

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

            Enigma.objects.create(ip_trail= bot_trail,
                                  pergunta= pergunta,
                                  resposta=resposta,
                                  next_ip=next_ip,
                                  current_ip=current_ip)

            a = Software.objects.create(userid=bot_trail, softname='secret',
                                    softversion=0,
                                    softsize=0,
                                    softram=0,
                                    softtype=typesoft, softhidden=0, softhiddenwith=0)




