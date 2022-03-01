from django.http import HttpResponse
from django.db.models import Q
import json
from app.models import Poste, AggHour, AggDay, AggMonth, AggYear, AggAll
from app.tools.jsonPlus import JsonPlus
import dateutil

# def viewLastAggMonth(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "M", poste_id, keys, nb_items)

# def viewAggHour(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "H", poste_id, keys, start_dt, end_dt)


# def viewLastAggHour(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "H", poste_id, keys, nb_items)

# def viewAggHour(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "H", poste_id, keys, start_dt, end_dt)


# def viewLastAggHour(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "H", poste_id, keys, nb_items)


# def viewAggDay(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "D", poste_id, keys, start_dt, end_dt)


# def viewLastAggDay(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "D", poste_id, keys, nb_items)


# def viewAggMonth(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "M", poste_id, keys, start_dt, end_dt)


# def viewLastAggMonth(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "M", poste_id, keys, nb_items)


# def viewAggYear(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "Y", poste_id, keys, start_dt, end_dt)


# def viewLastAggYear(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "Y", poste_id, keys, nb_items)


# def viewAggGlobal(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
#     return viewAgg(request, "A", poste_id, keys, start_dt, end_dt)


# def viewLastAggGlobal(request, poste_id, keys: str = '*', nb_items: int = 1):
#     return viewLastAgg(request, "A", poste_id, keys, nb_items)


def load_agg_info(agg_result: json, j: json, keys: list):
    if j.items().__len__() == 0:
        return "...... *** NO DATA ***"
    for key, value in j.items():
        if key == 'dv':
            continue
        if keys[0] == '*':
            agg_result[key] = value
            continue
        for onekey in keys:
            if key.startswith(onekey):
                agg_result[key] = value
                continue


def display_data_all(result: json, ah_all: list, keys: list):
    for one_agg in ah_all:
        duration_percent = (one_agg.duration_sum / one_agg.duration_max) * 100
        one_result = {'id': one_agg.id, 'start_dat': one_agg.start_dat, 'duration_sum': one_agg.duration_sum, 'duration %': duration_percent, 'keys': {}}
        load_agg_info(one_result['keys'], one_agg.j, keys)
        result['aggregations'].append(one_result)


def viewLastAgg(request, agg_niveau, poste_id, str_keys: str = '*', nb_items: int = 0, is_tmp: bool = None):
    # keys prefix to lookup
    keys = []
    for a_k in str_keys.split(','):
        keys.append(a_k)
    # get our poste
    p = Poste.objects.get(id=poste_id)
    result = {'poste_id': p.id, 'meteor': p.meteor, 'level': agg_niveau, 'aggregations': []}
    if agg_niveau == "H":
        ah = AggHour.objects.filter(~Q(duration_sum=0), poste_id=poste_id).order_by('-start_dat')[:nb_items][::-1]
        display_data_all(result, ah, keys)
    elif agg_niveau == "D":
        ah = AggDay.objects.filter(~Q(duration_sum=0), poste_id=poste_id).order_by('-start_dat')[:nb_items][::-1]
        display_data_all(result, ah, keys)
    elif agg_niveau == "M":
        ah = AggMonth.objects.filter(~Q(duration_sum=0), poste_id=poste_id).order_by('-start_dat')[:nb_items][::-1]
        display_data_all(result, ah, keys)
    elif agg_niveau == "Y":
        ah = AggYear.objects.filter(~Q(duration_sum=0), poste_id=poste_id).order_by('-start_dat')[:nb_items][::-1]
        display_data_all(result, ah, keys)
    elif agg_niveau == "A":
        ah = AggAll.objects.filter(~Q(duration_sum=0), poste_id=poste_id)[:nb_items][::-1]
        display_data_all(result, ah, keys)
    else:
        result['aggregations'].appent({'info': ' ** Aggregation Level Error: ' + str(agg_niveau)})
    return HttpResponse(JsonPlus().dumps(result))


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
        ah = AggHour.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat, start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "D":
        ah = AggDay.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat, start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "M":
        ah = AggMonth.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat, start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "Y":
        ah = AggYear.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat, start_dat__lte=end_date).order_by("start_dat").all()
        display_data_all(result, ah, keys)
    elif agg_niveau == "A":
        ah = (AggAll.objects.filter(poste_id=poste_id).first(), )
        display_data_all(result, ah, keys)
    else:
        result['aggregations'].appent({'info': ' ** Aggregation Level Error: ' + str(agg_niveau)})
    return HttpResponse(JsonPlus().dumps(result))
