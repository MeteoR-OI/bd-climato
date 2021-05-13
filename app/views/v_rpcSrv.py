from django.http import HttpResponse
from app.classes.workers.workerRoot import WorkerRoot
from app.tools.climConstant import SvcRequestType
from app.tools.jsonPlus import JsonPlus
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def viewControlSvc(request):
    j_request = JsonPlus().loads(request.body)
    j_resp = {"status": "?", "result": [], "errMsg": []}

    try:
        my_cde = j_request['cde']
        if (my_cde & SvcRequestType.List) == SvcRequestType.List:
            list_services(j_resp)

        svc_instance = getSvcInstance(j_request['svc'])
        if svc_instance is None:
            return

        trace_flag = False

        # process tracing changes request
        if ((my_cde & SvcRequestType.TraceOn) == SvcRequestType.TraceOn) or ((my_cde & SvcRequestType.TraceOff) == SvcRequestType.TraceOff):
            trace_flag = (my_cde & SvcRequestType.TraceOn) == SvcRequestType.TraceOn
            svc_instance.SetTraceFlag(trace_flag)
            j_resp['status'] = 'ok'
            if trace_flag is True:
                j_resp['result'].append('service ' + j_request['svc'] + ' is traced')
            else:
                j_resp['result'].append('service ' + j_request['svc'] + ' is not traced anymore')

        params = {}
        if j_request.get('params') is not None:
            params = j_request['params']
        params['trace_flag'] = trace_flag

        svc_control = SvcRequestType.Start | SvcRequestType.Stop | SvcRequestType.Status | SvcRequestType.Run
        if (my_cde & svc_control) != SvcRequestType.Nope:
            ControlSvc(j_resp, svc_instance, my_cde, params)

    except Exception as inst:
        j_resp = {"status": "err", "message": str(inst)}

    finally:
        if j_resp['errMsg'].__len__() == 0:
            del j_resp['errMsg']
        return HttpResponse(JsonPlus().dumps(j_resp))


def getSvcInstance(name: str):
    all_syn = WorkerRoot.GetSynonym()
    for a_syn in all_syn:
        if name == a_syn['name']:
            return a_syn['instance']
        for one_syn in a_syn['s']:
            if name == one_syn:
                return a_syn['instance']
    return None


def ControlSvc(j_resp: dict, svc_instance, cde: SvcRequestType, params: json = {}):
    try:
        j_resp['status'] = 'ok'
        if (cde & SvcRequestType.Run) == SvcRequestType.Run:
            svc_instance.RunIt(params)
            j_resp['result'].append('service ' + svc_instance.display + ' activated')
            return True

        if (cde & SvcRequestType.Start) == SvcRequestType.Start:
            svc_instance.Start()
            j_resp['result'].append('service ' + svc_instance.display + ' started')
            return True

        if (cde & SvcRequestType.Stop) == SvcRequestType.Stop:
            svc_instance.Stop()
            j_resp['result'].append('service ' + svc_instance.display + ' stopped')
            return True

        if (cde & SvcRequestType.Status) == SvcRequestType.Status:
            st = svc_instance.IsRunning()
            if st:
                status = 'is running'
            else:
                status = 'is stopped'
            j_resp['result'].append('service ' + svc_instance.display + ' ' + status)
            return True
        return True
    except Exception as inst:
        j_resp['status'] = 'err'
        j_resp['errMsg'] = 'Exception: ' + str(inst)
        return False


def list_services(j_resp: dict):
    try:
        j_resp['result'].append('list Services:')
        all_syn = WorkerRoot.GetSynonym()
        for a_syn in all_syn:
            svc_names = '  ' + a_syn['name']
            b_first = False
            for a_syno in a_syn['s']:
                if b_first is False:
                    b_first = True
                    svc_names += ' synonymes: '
                svc_names += a_syno + ', '
            if b_first:
                svc_names = svc_names[0:-2]
            j_resp['result'].append(svc_names)
        j_resp['status'] = 'ok'
        return True
    except Exception as inst:
        j_resp['status'] = 'err'
        j_resp['errMsg'].append('--list Error: ' + str(inst))
