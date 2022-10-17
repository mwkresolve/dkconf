from django.contrib import admin
from .models import *

@admin.register(HackedDatabase)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'iphacked')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'bio', 'gamepass', 'gameip', 'net', 'money', 'ipconnected', 'log')

@admin.register(Processes)
class LogAdmin(admin.ModelAdmin):
    list_display = ('userid', 'action', 'timestart', 'timeend', 'logedit', 'iptryhack', 'completed')


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('serverid','userid', 'cpu', 'hdd', 'ram')



@admin.register(TypeSofts)
class TypeSoftAdmin(admin.ModelAdmin):
    list_display = ('type',)


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('userid', 'softname','softversion','softsize','softram','softtype','softhidden','softhiddenwith' )
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    softname = models.CharField(max_length=25)
    softversion = models.IntegerField()
    softsize = models.IntegerField()
    softram = models.IntegerField()
    softtype = models.ForeignKey(TypeSofts, on_delete=models.CASCADE)
    softhidden = models.BooleanField()  # Field name made lowercase.
    softhiddenwith = models.BigIntegerField(default=0)  # Field name made lowercase.



admin.site.register(UserStats)
admin.site.register(CacheUser)
admin.site.register(HistUsersCurrent)
from django.contrib import admin

# Register your models here.
