from django.http import HttpResponse
import json
from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
from app.classes.integrationTests.typeTemp import TypeTempTest
from app.tools.jsonPlus import JsonPlus
import dateutil


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


def view_agg_hour(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "H", poste_id, keys, start_dt, end_dt)


def testComputeJ0(request):
    """ debug environment"""
    try:
        tt = TypeTempTest()
        ret_json = tt.doCalculusJ0()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def testComputeJ1(request):
    """ debug environment"""
    try:
        tt = TypeTempTest()
        ret_json = tt.doCalculusJ1()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def testComputeJ2(request):
    """ debug environment"""
    try:
        tt = TypeTempTest()
        ret_json = tt.doCalculusJ2()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def testComputeJ3(request):
    """ debug environment"""
    try:
        tt = TypeTempTest()
        ret_json = tt.doCalculusJ3()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def testComputeJ4(request):
    """ debug environment"""
    try:
        tt = TypeTempTest()
        ret_json = tt.doCalculusJ4()
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def view_agg_day(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "D", poste_id, keys, start_dt, end_dt)


def view_agg_month(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "M", poste_id, keys, start_dt, end_dt)


def view_agg_year(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "Y", poste_id, keys, start_dt, end_dt)


def view_agg_all(request, poste_id, keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    return view_agg(request, "A", poste_id, keys, start_dt, end_dt)


def display_data_key(j: json, keys: list):
    data_out = ''
    if j.items().__len__() == 0:
        return "...... *** NO DATA ***"
    for key, value in j.items():
        if key == 'dv':
            continue
        if keys[0] == '*':
            data_out = data_out + "......" + key + ': ' + str(value) + '<p>'
            continue
        for onekey in keys:
            if key.startswith(onekey):
                data_out = data_out + "......" + key + ': ' + str(value) + '<p>'
                continue
    return data_out


def display_data_all(header: str, ah_all: list, keys: list):
    result = ''
    for one_agg in ah_all:
        result = result + header + ', id: ' + str(one_agg.id) + ', dat: ' + str(one_agg.start_dat) + '<p>'
        result = result + display_data_key(one_agg.j, keys) + '<p>'
    return result


def view_agg(request, agg_niveau, poste_id, str_keys: str = '*', start_dt: str = '1900-01-11 00:00:00+04', end_dt: str = '2100-12-31 23:59:00+04'):
    start_dat = dateutil.parser.parse(str(start_dt.replace('|', ' ')))
    end_date = dateutil.parser.parse(str(end_dt.replace('|', ' ')))
    keys = []
    for a_k in str_keys.split(','):
        keys.append(a_k)
    p = Poste.objects.get(id=poste_id)
    header = 'poste_id: ' + str(p.id) + ', meteor: <b>' + p.meteor + '</b>'
    if agg_niveau == "H":
        ah = Agg_hour.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        result_display = display_data_all(header, ah, keys)
    elif agg_niveau == "D":
        ah = Agg_day.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        result_display = display_data_all(header, ah, keys)
    elif agg_niveau == "M":
        ah = Agg_month.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        result_display = display_data_all(header, ah, keys)
    elif agg_niveau == "Y":
        ah = Agg_year.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        result_display = display_data_all(header, ah, keys)
    elif agg_niveau == "A":
        ah = Agg_global.objects.filter(poste_id=poste_id).filter(start_dat__gte=start_dat).filter(start_dat__lte=end_date).order_by("start_dat").all()
        result_display = display_data_all(header, ah, keys)
    else:
        result_display = '@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%<p>'
        result_display = result_display + 'poste_id: ' + str(p.id) + ', meteor: ' + p.meteor + ' ** Aggregation Level Error: ' + str(agg_niveau) + '<p>'
        result_display = result_display + '@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%<p>'
    return HttpResponse(result_display)
