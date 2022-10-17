from django.shortcuts import render

from controller.models import HackedDatabase


def dbview(request):
    ips_user = HackedDatabase.objects.filter(userid=request.user).values()
    return render(request, 'hackeddb.html', {'ipshacked': ips_user})
