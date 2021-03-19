from django.http import HttpResponse
import json
from app.models import Poste, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
from app.tools.jsonPlus import JsonPlus
import dateutil


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


def load_agg_info(agg_result: list, j: json, keys: list):
    if j.items().__len__() == 0:
        return "...... *** NO DATA ***"
    for key, value in j.items():
        if key == 'dv':
            continue
        if keys[0] == '*':
            agg_result.append({'key': key, 'value': value})
            continue
        for onekey in keys:
            if key.startswith(onekey):
                agg_result.append({'key': key, 'value': value})
                continue


def display_data_all(result: json, ah_all: list, keys: list):
    for one_agg in ah_all:
        one_result = {'id': one_agg.id, 'start_dat': one_agg.start_dat, 'keys': []}
        load_agg_info(one_result['keys'], one_agg.j, keys)
        result['aggregations'].append(one_result)


def view_agg(request, agg_niveau, poste_id, str_keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    # replace the | by space (for dates passed in the url)
    start_dat = dateutil.parser.parse(str(start_dt.replace('|', ' ')))
    end_date = dateutil.parser.parse(str(end_dt.replace('|', ' ')))
    # keys prefix to lookup
    keys = []
    for a_k in str_keys.split(','):
        keys.append(a_k)
    # get our poste
    p = Poste.objects.get(id=poste_id)
    result = {'poste_id': p.id, 'meteor': p.meteor, 'level': agg_niveau, 'aggregations': []}
    if agg_niveau == "H":
        ah = Agg_hour.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "D":
        ah = Agg_day.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "M":
        ah = Agg_month.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "Y":
        ah = Agg_year.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "A":
        ah = Agg_global.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    else:
        result['aggregations'].appent({'info': ' ** Aggregation Level Error: ' + str(agg_niveau)})
    return HttpResponse(JsonPlus().dumps(result))
