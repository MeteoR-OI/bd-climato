# from app.classes.workers.svcLoadJson import SvcJsonLoader
# from app.classes.workers.svcMigrate import SvcMigrate
# import app.classes.workers
from app.tools.refManager import RefManager
from django.http import HttpResponse
from app.tools.jsonPlus import JsonPlus
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def viewControlSvc(request):
    j_request = json.loads(request.body)
    j_resp = {"status": "?", "result": []}

    try:
        svc_ctrl = SvcCtrl()
        svc_name = None if j_request.get('svc') is None else j_request['svc'].lower()
        action = None if j_request.get('action') is None else j_request['action'].lower()
        params = j_request['params']

        j_resp['status'] = 'ok'

        if action == 'list':
            j_resp['result'] = svc_ctrl.ListSvc()
            return

        svc_instance = svc_ctrl.GetSvcInstance(svc_name)

        if action == 'run':
            svc_instance.RunMe(params)
            j_resp['result'] = ['service activated']
            return

        if action == 'start':
            svc_instance.Start()
            j_resp['result'] = ['service started']
            return

        if action == 'stop':
            svc_instance.Stop()
            j_resp['result'] = ['service stopped']
            return

        if action == 'add_param':
            svc_instance.AddWorkItem(params)
            j_resp['result'] = ['parameter added to the service queue']
            return

        if action == 'status':
            if svc_instance.IsRunning() is True:
                j_resp['result'] = ['service is started']
            else:
                j_resp['result'] = ['service is stopped']
            return

        raise Exception('unknown action')

    except Exception as inst:
        j_resp = {"status": "err", "result": [str(inst)]}

    finally:
        return HttpResponse(JsonPlus().dumps(j_resp))


class SvcCtrl:
    class_info = []

    def __init__(self):
        self.class_info = RefManager.GetInstance().ListRefs()

    def GetSvcInstance(self, name):
        for k in self.class_info:
            if str(k).startswith('Inst_'):
                tmp_name = self.class_info[k].GetDisplayName()
                if tmp_name.startswith('svc'):
                    tmp_name = str(tmp_name[3:]).lower()
                if tmp_name == name:
                    return self.class_info[k]
        raise Exception('service ' + name + ' not found')

    def ListSvc(self):
        svc_list = []
        for k in self.class_info:
            if str(k).startswith('Inst_'):
                tmp_name = self.class_info[k].GetDisplayName().lower()
                if tmp_name.startswith('svc'):
                    tmp_name = str(tmp_name[3:])
                svc_list.append(tmp_name)
        return svc_list

# svc_loader = SvcJsonLoader()
# svc_loader.Start()
# svc_loader.RunMe()

# svc_migrate = SvcMigrate()
# svc_migrate.Start()
# svc_migrate.AddWorkItem("BBF015")
# svc_migrate.RunMe()
