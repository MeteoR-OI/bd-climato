#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
from app.classes.calcul.calcAggreg import CalcAggreg
import os


def view_my_recalc(request, file_name):
    view_my_calc(request, file_name, True)


# views to update
def view_my_calc(request, file_name, is_tmp: bool = False):
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ret_json = loadJson(base_dir + '/../data/json_not_in_git/' + file_name, False, True, is_tmp)
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)
        # print(inst.args)     # arguments stored in .args
        # print(inst)          # __str__ allows args to be printed directly,


def loadJson(file_name: str, delete_flag: bool, trace_flag: bool, is_tmp: bool = None):
    calc_obs = CalcObs()
    texte = ''

    with open(file_name, "r") as f:
        lignes = f.readlines()
        for aligne in lignes:
            texte += str(aligne)

        my_json_array = JsonPlus().loads(texte)
        ret = calc_obs.loadJson(my_json_array, delete_flag, trace_flag, is_tmp)

        # start in sync the calculus if our aggregations
        CalcAggreg().ComputeAggreg(is_tmp)
        # SvcAggreg.GetInstance().RunIt()
        return {'loadObs': ret, 'svcAgg': 'done'}
