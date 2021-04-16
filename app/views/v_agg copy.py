from django.http import HttpResponse
import json
from app.models import Poste, AggHour, AggDay, AggMonth, AggYear, AggAll, TmpAggHour, TmpAggDay, TmpAggMonth, TmpAggYear, TmpAggAll
from app.tools.jsonPlus import JsonPlus
import dateutil


def viewAggHour(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, "H", poste_id, keys, start_dt, end_dt)


def viewAggDay(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, "D", poste_id, keys, start_dt, end_dt)


def viewAggMonth(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, "M", poste_id, keys, start_dt, end_dt)


def viewAggYear(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, "Y", poste_id, keys, start_dt, end_dt)


def viewAggGlobal(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return viewAgg(request, "A", poste_id, keys, start_dt, end_dt)


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


def viewAgg(request, agg_niveau, poste_id, str_keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04', is_tmp: bool = None):
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
        ah = AggHour.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "D":
        ah = AggDay.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "M":
        ah = AggMonth.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "Y":
        ah = AggYear.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "A":
        ah = AggAll.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "HT":
        ah = TmpAggHour.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "DT":
        ah = TmpAggDay.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "MT":
        ah = TmpAggMonth.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "YT":
        ah = TmpAggYear.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "AT":
        ah = TmpAggAll.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    else:
        result['aggregations'].appent({'info': ' ** Aggregation Level Error: ' + str(agg_niveau)})
    return HttpResponse(JsonPlus().dumps(result))
