from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max
from gameinternet.views import hackip
from controller.functionsdb import *


def tasks_view(request):
    print('chegou tasks')
    tasks = Processes.objects.filter(userid=request.user).values()
    tasks_not_complet = Processes.objects.filter(userid=request.user, completed=False).values()

    return render(request, "tasks.html", {'tasks': tasks, 'sem_task': len(tasks_not_complet)})


def complete_task(request):
    get_id = request.get_full_path().split('%3D')[1]
    task = Processes.objects.filter(userid=request.user, id=get_id).values()
    ip_connect = User.objects.filter(username=request.user).values('ipconnected')[0]['ipconnected']
    # garantir que somente vai manipular as proprias tasks
    if len(task) > 0:
        # garantir que nao vai rodar processo ja concluido
        for infos in task:
            if not infos['completed']:
                if infos['action'] == 1:  # action editar log

                    if infos['ismyserver']:
                        edit_my_log(request.user, infos['logedit'])
                        User.objects.filter(username=request.user).update(log=infos['logedit'])
                        Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                        return HttpResponseRedirect("log/")

                    else:
                        # ip_connect
                        edit_log_victim(gameip_victim=ip_connect, logedit=infos['logedit'])
                        Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    return HttpResponseRedirect("internet")
                if infos['action'] == 2:  # tentar hackear ip
                    ip_victim = infos['iptryhack']
                    softs_user = Software.objects.filter(userid=request.user, softtype_id=1).values()
                    maxlvl_crc_user = softs_user.aggregate(Max('softversion'))['softversion__max']
                    victim = User.objects.filter(gameip=ip_victim).values_list('id')[0][0]
                    softs_victim = Software.objects.filter(userid=victim, softtype_id=2).values_list()
                    maxlvl_hash_victim = softs_victim.aggregate(Max('softversion'))['softversion__max']
                    if not maxlvl_hash_victim:
                        maxlvl_hash_victim = 0

                    if maxlvl_crc_user >= maxlvl_hash_victim:
                        HackedDatabase.objects.create(userid=request.user, iphacked=ip_victim)
                        Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                        msgbroke = """<span style="color: green"> Você conseguiu hackear o servidor</span>"""
                        return hackip(request, msgbroke, ip_victim)
                    else:

                        Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                        msgbroke = """<span style="color: red"> Seu cracker não é bom o suficiente</span>"""
                        return hackip(request, msgbroke, ip_victim)

                if infos['action'] == 3:  # download soft
                    # impedir download proprio soft, impedir download soft igual
                    softdown = Software.objects.filter(id=infos['softdownload']).values()
                    typeofsoft = TypeSofts.objects.get(id=softdown[0]['softtype_id'])
                    Software.objects.create(
                        userid=request.user,
                        softname=softdown[0]['softname'],
                        softversion=softdown[0]['softversion'],
                        softsize=softdown[0]['softsize'],
                        softram=softdown[0]['softram'],
                        softtype=typeofsoft)
                    log_edit = f'''$ {request.user.gameip} download {softdown[0]['softname']}{typeofsoft} Version: {softdown[0]['softversion']} '''
                    edit_log_usr_and_victim(user=request.user,
                                            gameip_victim=infos['ipvictim'],
                                            logedit=log_edit)

                    # download concluido
                    Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    return HttpResponseRedirect("/software/")

                if infos['action'] == 4:  # del soft
                    softdeleted = Software.objects.filter(id=infos['softdel']).values()
                    soft_name = softdeleted[0]['softname']
                    soft_version = softdeleted[0]['softversion']

                    if infos['delmysoft']:
                        print('meu soft')
                        softdel = Software.objects.filter(id=infos['softdel'])
                        softdel.delete()
                        update_reputation(request.user, 50)
                        log_edit = f'''$ {request.user.gameip} deleted {soft_name} Version:{soft_version} '''
                        edit_my_log(user=request.user, logedit=log_edit, oldlog=True)
                        Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                        return HttpResponseRedirect("/software/")
                    softdel = Software.objects.filter(id=infos['softdel'])
                    softdel.delete()
                    update_reputation(request.user, 50)
                    log_edit = f'''$ {request.user.gameip} deleted {soft_name} Version:{soft_version} '''
                    edit_log_usr_and_victim(user=request.user,
                                            gameip_victim=infos['ipvictim'],
                                            logedit=log_edit)
                    Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    return HttpResponseRedirect("/internet/")

                if infos['action'] == 5:  # upload soft
                    # criar condicao soft duplicado etc...
                    softupload = Software.objects.filter(id=infos['softupload']).values()
                    ip_upload = User.objects.filter(gameip=infos['uploadip'])[0]
                    typeofsoft = TypeSofts.objects.get(id=softupload[0]['softtype_id'])
                    Software.objects.create(
                        userid=ip_upload,
                        softname=softupload[0]['softname'],
                        softversion=softupload[0]['softversion'],
                        softsize=softupload[0]['softsize'],
                        softram=softupload[0]['softram'],
                        softtype=typeofsoft)
                    update_reputation(request.user, 50)
                    log_edit = f'''$ {request.user.gameip} upload {softupload[0]['softname']} Version:{softupload[0]['softversion']} '''
                    edit_log_usr_and_victim(user=request.user,
                                            gameip_victim=infos['uploadip'],
                                            logedit=log_edit)

                    Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    return HttpResponseRedirect("/internet/")
                if infos['action'] == 6:  # run soft
                    info_soft = Software.objects.filter(id=infos['softrun']).values()[0]
                    typeofsoft = TypeSofts.objects.get(id=info_soft['softtype_id'])
                    softrun = infos['softrun']
                    Software.objects.filter(id=softrun).update(isactive=True)
                    Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    if infos['ismyserver']:
                        log_edit = f'''$ {request.user.gameip} run {info_soft['softname']}{typeofsoft} Version:{info_soft['softversion']} on localhost '''
                        edit_my_log(user=request.user, logedit=log_edit, oldlog=True)
                        return HttpResponseRedirect("/software/")
                    log_edit = f'''$ {request.user.gameip} run {info_soft['softname']}{typeofsoft} Version:{info_soft['softversion']} on host {infos['ipvictim']} '''
                    edit_log_usr_and_victim(user=request.user,
                                            gameip_victim=infos['ipvictim'],
                                            logedit=log_edit)

                    return HttpResponseRedirect("/internet/")
                if infos['action'] == 7:  # stop soft
                    softstop = infos['softstop']
                    info_soft = Software.objects.filter(id=softstop).values()[0]
                    typeofsoft = TypeSofts.objects.get(id=info_soft['softtype_id'])
                    Software.objects.filter(id=softstop).update(isactive=False)
                    Processes.objects.filter(userid=request.user, id=get_id).update(completed=True)
                    if infos['ismyserver']:
                        log_edit = f'''$ {request.user.gameip} stop {info_soft['softname']}{typeofsoft} Version:{info_soft['softversion']} on localhost '''
                        edit_my_log(user=request.user, logedit=log_edit, oldlog=True)
                        return HttpResponseRedirect("/software/")
                    log_edit = f'''$ {request.user.gameip} stop {info_soft['softname']}{typeofsoft} Version:{info_soft['softversion']} on host {infos['ipvictim']} '''
                    edit_log_usr_and_victim(user=request.user,
                                            gameip_victim=infos['ipvictim'],
                                            logedit=log_edit)
                    return HttpResponseRedirect("/internet/")
    else:
        print('esse processo  não é seu')

    return render(request, "tasks.html")
