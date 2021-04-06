#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calculus import AllCalculus
import os


# views to update
def view_my_calc(request, file_name):
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ret_json = loadJson(base_dir + '/../data/json_not_in_git/' + file_name, False, True)
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)
        # print(inst.args)     # arguments stored in .args
        # print(inst)          # __str__ allows args to be printed directly,


def loadJson(file_name: str, delete_flag: bool, trace_flag: bool):
    calc = AllCalculus()
    texte = ''

    with open(file_name, "r") as f:
        lignes = f.readlines()
        for aligne in lignes:
            texte += str(aligne)

        my_json = JsonPlus().loads(texte)
        ret = calc.loadJson(my_json, delete_flag, trace_flag)
        return ret
