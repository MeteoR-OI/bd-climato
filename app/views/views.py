#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.models import Poste, Observation
from app.views.v_agg import viewAgg, viewLastAgg
from app.views.v_poste import view_my_poste
from app.views.v_calc import view_my_calc
from app.views.v_rpcSrv import viewControlSvc
from app.views.v_api import view_stations_list, view_stations_data
from django.views.decorators.csrf import csrf_exempt
import json


# views well routed
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def view_control_svc(request):
    return viewControlSvc(request)


def viewStationList(request):
    return view_stations_list(request)


def viewStationData(request, station: str = None):
    return view_stations_data(request, station)


def view_agg(request, period: str, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, period.upper(), poste_id, keys, start_dt, end_dt)


def view_last_agg(request, period: str, poste_id, keys: str = '*', nb_items: int = 1):
    return viewLastAgg(request, period.upper(), poste_id, keys, nb_items)


def view_poste(request, poste_id):
    return view_my_poste(request, poste_id)


def views_calc(request, file_name: str):
    return view_my_calc(request, file_name, False)


def views_recalc(request, file_name: str):
    return view_my_calc(request, file_name, True)


def view_last_obs(request, poste_id):
    p = Poste.objects.get(id=poste_id)
    o = Observation.objects.filter(poste_id=poste_id).order_by("dat").last()
    data_details = {'poste_id': p.id, 'meteor': p.meteor, 'dat': str(o.dat), 'rain': str(o.j['rain'])}
    return HttpResponse(json.dumps(data_details))
