#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
import json
from app.models import Poste, Observation
from app.views.v_agg import view_agg
from app.views.v_poste import view_my_poste
from app.views.v_calc import view_my_calc


# views well routed
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def view_agg_hour(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "H", poste_id, keys, start_dt, end_dt)


def view_agg_day(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "D", poste_id, keys, start_dt, end_dt)


def view_agg_month(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "M", poste_id, keys, start_dt, end_dt)


def view_agg_year(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "Y", poste_id, keys, start_dt, end_dt)


def view_agg_all(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "A", poste_id, keys, start_dt, end_dt)


def view_poste(request, poste_id):
    return view_my_poste(request, poste_id)


def views_calc(request, file_name: str):
    return view_my_calc(request, file_name)


def view_last_obs(request, poste_id):
    p = Poste.objects.get(id=poste_id)
    o = Observation.objects.filter(poste_id=poste_id).order_by("dat").last()
    data_details = {'poste_id': p.id, 'meteor': p.meteor, 'dat': str(o.dat), 'rain': str(o.j['rain'])}
    return HttpResponse(json.dumps(data_details))
