#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.models import Poste, Observation
import json
from app.tools.jsonPlus import JsonPlus
import dateutil


def view_obs_data(request, poste_id, str_keys: str, start_dt: str, end_dt: str):
    # start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'
    # keys prefix to lookup
    keys = []
    for a_k in str_keys.split(','):
        keys.append(a_k)
    p = Poste.objects.get(id=poste_id)
    if start_dt is None:
        obs_data = (Observation.objects.filter(poste_id=poste_id).order_by("stop_dat").last(),)
    else:
        start_dat = dateutil.parser.parse(str(start_dt.replace('|', ' ')))
        if end_dt is None:
            end_date = '2100-12-31 23:59:00+04'
        else:
            end_date = dateutil.parser.parse(str(end_dt.replace('|', ' ')))
        obs_data = Observation.objects.filter(poste_id=poste_id).filter(stop_dat__gte=start_dat, stop_dat__lte=end_date).order_by("stop_dat").all()

    data_details = {'poste_id': p.id, 'meteor': p.meteor, 'obs': []}
    for one_obs in obs_data:
        one_result = {'id': one_obs.id, 'stop_dat': str(one_obs.stop_dat), 'duration': one_obs.duration, 'obs': {}, 'pre_agg': []}
        load_agg_info(one_result['obs'], one_result['pre_agg'], one_obs.j, one_obs.j_agg, keys)
        data_details['obs'].append(one_result)

    return HttpResponse(JsonPlus().dumps(data_details), content_type="application/json")


def load_agg_info(agg_result: json, pre_agg: json, j: json, j_agg: list, keys: list):
    if j.__len__() > 0:
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

    for a_jagg in j_agg:
        if a_jagg.__len__() > 0:
            tmp_agg = {}
            for key, value in a_jagg.items():
                if key == 'dv':
                    continue
                if key == 'level' or key == 'start_dat':
                    tmp_agg[key] = value
                    continue
                if keys[0] == '*':
                    tmp_agg[key] = value
                    continue
                for onekey in keys:
                    if key.startswith(onekey):
                        tmp_agg[key] = value
                        continue
            if tmp_agg.__len__() > 0:
                pre_agg.append(tmp_agg)
