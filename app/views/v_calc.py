#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
from app.classes.calcul.calcAggreg import CalcAggreg
from app.classes.workers.svcAggreg import SvcAggreg
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.metier.posteMetier import PosteMetier
import os
import datetime


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
        agg_j_ret = {'loadObs': ret}
        if is_tmp is True:
            t_start = datetime.datetime.now()
            agg_todo_count = AggTodoMeteor(99999999, is_tmp).count()
            CalcAggreg().ComputeAggreg(is_tmp)
            t_end = datetime.datetime.now()
            agg_j_ret['loadAgg'] = {'total_exec': str(t_end - t_start)}
            agg_j_ret['item_processed'] = str(agg_todo_count)
            agg_j_ret['one_exec'] = str((t_end - t_start)/agg_todo_count)
        else:
            SvcAggreg.runMe()
            agg_j_ret['loadAgg'] = 'started'

        # SvcAggreg.GetInstance().RunIt()

        return agg_j_ret
