from django.http import HttpResponse
import json
from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from app.classes.tests.typeTemp_test import type_temp_test
from app.tools.JsonPlus import JsonPlus


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def view_poste(request, poste_id):
    p = Poste.objects.get(id=poste_id)
    data_details = {'function': 'last_obs', 'poste_id': p.id, 'meteor': p.meteor, 'owner': p.owner}
    return HttpResponse(json.dumps(data_details))


def view_last_obs(request, poste_id):
    p = Poste.objects.get(id=poste_id)
    o = Observation.objects.filter(poste_id=poste_id).order_by("dat").last()
    data_details = {'poste_id': p.id, 'meteor': p.meteor, 'dat': str(o.dat), 'rain': str(o.j['rain'])}
    return HttpResponse(json.dumps(data_details))


def view_agg_hour(request, poste_id):
    return view_agg(request, "H", poste_id)


def test_compute(request):
    """ debug environment"""
    try:
        tt = type_temp_test()
        ret_json = tt.load_obs()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def test_compute_agg(request):
    """ debug environment"""
    try:
        tt = type_temp_test()
        ret_json = tt.load_agg()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def test_getset(request):
    """ debug environment"""
    try:

        tt = type_temp_test()
        ret_json = tt.getset()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def view_agg_day(request, poste_id):
    return view_agg(request, "D", poste_id)


def view_agg_month(request, poste_id):
    return view_agg(request, "M", poste_id)


def view_agg_year(request, poste_id):
    return view_agg(request, "Y", poste_id)


def view_agg_all(request, poste_id):
    return view_agg(request, "A", poste_id)


def view_agg(request, agg_niveau, poste_id):
    data_details = {}
    p = Poste.objects.get(id=poste_id)
    if agg_niveau == "H":
        ah = Agg_hour.objects.filter(poste_id=poste_id).order_by("dat").last()
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'hour', 'dat': str(ah.dat), 'rain': str(ah.j['rain'])}
    elif agg_niveau == "D":
        ah = Agg_day.objects.filter(poste_id=poste_id).order_by("dat").last()
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'day', 'dat': str(ah.dat), 'rain': str(ah.j['rain'])}
    elif agg_niveau == "M":
        ah = Agg_month.objects.filter(poste_id=poste_id).order_by("dat").last()
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'month', 'dat': str(ah.dat), 'rain': str(ah.j['rain'])}
    elif agg_niveau == "Y":
        ah = Agg_year.objects.filter(poste_id=poste_id).order_by("dat").last()
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'year', 'dat': str(ah.dat), 'rain': str(ah.j['rain'])}
    elif agg_niveau == "A":
        ah = Agg_global.objects.filter(poste_id=poste_id).order_by("dat").last()
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'all', 'dat': str(ah.dat), 'rain': str(ah.j['rain'])}
    else:
        data_details = {'poste_id': p.id, 'meteor': p.meteor, 'by': 'Aggregation Level Error ' + agg_niveau}
    return HttpResponse(json.dumps(data_details))
