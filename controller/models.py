from django.contrib.auth.models import AbstractUser
from django.db import models
from my_tools.functions import pwd_generator, ip_generator
from django.utils import timezone


class User(AbstractUser):
    bio = models.TextField(blank=True)
    gamepass = models.CharField(max_length=10, default='')
    gameip = models.CharField(max_length=20, default=ip_generator(), unique=True)
    premium = models.BooleanField(default=False)
    stats_game = models.BooleanField(default=False) # true if table depends created
    net = models.IntegerField(default=1)
    money = models.IntegerField(default=10000)
    isnpc = models.BooleanField(default=False)
    ipconnected = models.CharField(max_length=20,  default='off')
    log = models.TextField(default=f'operating system created at {timezone.now()}')

    def __str__(self):
        return self.username


    def get_tasks(self):
        return Processes.objects.filter(userid=self.id, completed=False).values()

class LastIp(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    ip = models.CharField(max_length=20, default='0.0.0.0')
    
    def __str__(self):
        return self.ip




class UserStats(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    datejoined = models.DateTimeField(db_column='dateJoined', default=timezone.now)  # Field name made lowercase.
    exp = models.IntegerField(default=0)
    certifications = models.CharField(max_length=30, default='ok')
    awards = models.CharField(max_length=50, default=0)
    timeplaying = models.FloatField(db_column='timePlaying', default=0)  # Field name made lowercase.
    missioncount = models.IntegerField(db_column='missionCount', default=0)  # Field name made lowercase.
    hackcount = models.IntegerField(db_column='hackCount', default=0)  # Field name made lowercase.
    ddoscount = models.IntegerField(db_column='ddosCount', default=0)  # Field name made lowercase.
    warezsent = models.FloatField(db_column='warezSent', default=0)  # Field name made lowercase.
    spamsent = models.BigIntegerField(db_column='spamSent', default=0)  # Field name made lowercase.
    bitcoinsent = models.FloatField(db_column='bitcoinSent', default=0)  # Field name made lowercase.
    ipresets = models.IntegerField(db_column='ipResets', default=0)  # Field name made lowercase.
    lastipreset = models.DateTimeField(db_column='lastIpReset', default=timezone.now)  # Field name made lowercase.
    pwdresets = models.IntegerField(db_column='pwdResets', default=0)  # Field name made lowercase.
    lastpwdreset = models.DateTimeField(db_column='lastPwdReset', default=timezone.now)  # Field name made lowercase.
    moneyearned = models.BigIntegerField(db_column='moneyEarned', default=0)  # Field name made lowercase.
    moneytransfered = models.BigIntegerField(db_column='moneyTransfered', default=0)  # Field name made lowercase.
    moneyhardware = models.BigIntegerField(db_column='moneyHardware', default=0)  # Field name made lowercase.
    moneyresearch = models.BigIntegerField(db_column='moneyResearch', default=0)  # Field name made lowercase.
    profileviews = models.IntegerField(db_column='profileViews', default=0)  # Field name made lowercase.

    def __str__(self):
        return str(self.user)

class Hardware(models.Model):
    serverid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, default='SERVER')
    cpu = models.FloatField(default=500)
    hdd = models.FloatField(default=100)
    ram = models.FloatField(default=256)

    def __str__(self):
        return f'serverid = {self.serverid}, userid = {self.userid}'




class CacheUser(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    reputation = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'log = {self.reputation}, userid = {self.userid}'



class HistUsersCurrent(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    reputation = models.BigIntegerField(default=0)
    age = models.IntegerField(default=0)
    clanid = models.IntegerField(default=0)  # Field name made lowercase.
    clanname = models.CharField( max_length=50, default='ok')  # Field name made lowercase.
    timeplaying = models.FloatField(default=0)  # Field name made lowercase.
    missioncount = models.IntegerField(default=0)  # Field name made lowercase.
    hackcount = models.IntegerField(default=0)  # Field name made lowercase.
    ddoscount = models.IntegerField(default=0)  # Field name made lowercase.
    ipresets = models.IntegerField(default=0)  # Field name made lowercase.
    moneyearned = models.BigIntegerField(default=0)  # Field name made lowercase.
    moneytransfered = models.BigIntegerField(default=0)  # Field name made lowercase.
    moneyhardware = models.BigIntegerField(default=0)  # Field name made lowercase.
    moneyresearch = models.BigIntegerField(default=0)  # Field name made lowercase.
    warezsent = models.PositiveIntegerField(default=0)  # Field name made lowercase.
    spamsent = models.PositiveIntegerField(default=0)  # Field name made lowercase.
    bitcoinsent = models.FloatField(default=0)  # Field name made lowercase.
    profileviews = models.PositiveIntegerField(default=0)  # Field name made lowercase.

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

class HackedDatabase(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    iphacked = models.CharField(max_length=20)



class Processes(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField()
    timestart = models.DateTimeField()
    timeend = models.DateTimeField()
    logedit = models.TextField(default='')
    iptryhack = models.CharField(max_length=20, default='')
    completed = models.BooleanField(default=False)
    softdownload = models.IntegerField(default=0)
    softupload = models.IntegerField(default=0)
    uploadip = models.CharField(max_length=20, default='')
    delmysoft =  models.BooleanField(default=False)
