from django.contrib.auth.models import AbstractUser
from django.db import models
from my_tools.functions import ip_generator
from django.utils import timezone


class User(AbstractUser):
    bio = models.TextField(blank=True)
    gamepass = models.CharField(max_length=10, default='')
    gameip = models.CharField(max_length=20, default=ip_generator(), unique=True)
    premium = models.BooleanField(default=False)
    stats_game = models.BooleanField(default=False)  # true if table depends created
    net = models.IntegerField(default=1)
    money = models.IntegerField(default=10000)
    isnpc = models.BooleanField(default=False)
    ipconnected = models.CharField(max_length=20, default='off')
    log = models.TextField(default=f'operating system created at {timezone.now()}')
    istrail = models.BooleanField(default=False)
    wallet_connect = models.CharField(max_length=100, default='off')
    account_bank_connect = models.CharField(max_length=100, default='off')

    def __str__(self):
        return self.username

    def get_tasks(self):
        return Processes.objects.filter(userid=self.id, completed=False).values()


class Enigma(models.Model):
    ip_trail = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    pergunta = models.CharField(max_length=30000, default='')
    resposta = models.CharField(max_length=30000, default='')
    current_ip = models.CharField(max_length=30000, default='')
    next_ip = models.CharField(max_length=30, default='')


class enigma_solved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enigma_ip = models.CharField(max_length=30000, default='')
    solved = models.BooleanField(default=False)


class LastIp(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    ip = models.CharField(max_length=20, default='0.0.0.0')

    def __str__(self):
        return self.ip



class Hardware(models.Model):
    serverid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, default='SERVER')
    cpu = models.FloatField(default=500)
    hdd = models.FloatField(default=100)
    ram = models.FloatField(default=256)

    def __str__(self):
        return f'serverid = {self.serverid}, userid = {self.userid}'


class HistUsersCurrent(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    reputation = models.BigIntegerField(default=0)

    def __str__(self):
        return f' userid = {self.userid}, reputation = {self.reputation}'


class TypeSofts(models.Model):
    type = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.type


class Software(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    softname = models.CharField(max_length=25)
    softversion = models.IntegerField()
    softsize = models.IntegerField()
    softram = models.IntegerField()
    softtype = models.ForeignKey(TypeSofts, on_delete=models.CASCADE)
    softhidden = models.BooleanField(default=0)  # Field name made lowercase.
    softhiddenwith = models.BigIntegerField(default=0)  # Field name made lowercase.
    isactive = models.BooleanField(default=False)


class HackedDatabase(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    iphacked = models.CharField(max_length=20)


class Processes(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    ipvictim = models.CharField(max_length=20, default='')
    action = models.IntegerField()
    timestart = models.DateTimeField()
    timeend = models.DateTimeField()
    logedit = models.TextField(default='')
    iptryhack = models.CharField(max_length=20, default='')
    softdownload = models.IntegerField(default=0)
    softupload = models.IntegerField(default=0)
    softdel = models.IntegerField(default=0)
    softrun = models.IntegerField(default=0)
    softstop = models.IntegerField(default=0)
    uploadip = models.CharField(max_length=20, default='')
    delmysoft = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    ismyserver = models.BooleanField(default=False)
