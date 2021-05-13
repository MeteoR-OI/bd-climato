#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
import os


def view_my_recalc(request, file_name):
    view_my_calc(request, file_name, True)


# views to update
def view_my_calc(request, file_name, is_tmp: bool = False):
    try:
        ret_json = _viewLoadJson(file_name, False, True, is_tmp), False
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def _viewLoadJson(file_name: str, delete_flag: bool, trace_flag: bool, is_tmp: bool = False, use_validation: bool = False):
    data = {
        "params": {
            "delete": delete_flag,
            "is_tmp": is_tmp,
            "validation": use_validation,
            "trace_flag": trace_flag,
            "base_dir": os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/../data/json_not_in_git/',
            "filename": file_name
        }
    }
    ret = CalcObs().LoadJsonFromSvc(data)
    return ret
