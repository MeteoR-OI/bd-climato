#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.http.response import JsonResponse
from django.db.models import Q
from app.tools.jsonPlus import JsonPlus
import json
from app.models import Poste, AggHour, AggDay, AggMonth, AggYear, AggAll


def view_stations_list(request):
    try:
        ret = serializers.serialize("json", Poste.objects.all())
        retJson = JsonResponse(ret, safe=False)
        return HttpResponse(retJson, content_type="application/json")

    except Exception as inst:
        return HttpResponse(inst)


def view_all_station_data(request):
    big_json = []
    try:
        all_postes = Poste.objects.all()
        for one_poste in all_postes:
            data_poste = get_data_for_one_station(one_poste.meteor)
            big_json.append(data_poste)
        return HttpResponse(json.dumps(big_json), content_type="application/json")

    except Exception as inst:
        return HttpResponse(inst)


def view_one_station_data(request, station: str = None):
    try:
        ret_json = get_data_for_one_station(station)
        return HttpResponse(json.dumps(ret_json), content_type="application/json")

    except Exception as inst:
        return HttpResponse(inst)


def get_data_for_one_station(station: str = None):
    try:
        if station is None:
            return HttpResponseBadRequest("no station given")
        mon_poste = Poste.objects.filter(meteor=station).values('id', 'meteor', 'fuseau', 'meteofr', 'owner', 'phone', 'email', 'address', 'zip', 'city', 'country', 'latitude', 'longitude')
        mon_poste_id = mon_poste[0]['id']
        if mon_poste is None:
            return HttpResponseBadRequest("station " + station + " not found")
        agg_hour = AggHour.objects.filter(~Q(duration_sum=0), poste_id=mon_poste_id).order_by('-start_dat').first()
        if agg_hour is None:
            return {
                "station": mon_poste[0],
                "data": {
                    "hour": {},
                    "day":  {},
                    "month":  {},
                    "year":  {},
                    "all":  {},
                }
            }
        agg_day = AggDay.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()
        agg_month = AggMonth.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()
        agg_year = AggYear.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()
        agg_all = AggAll.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()
        ret_json = {
            "station": mon_poste[0],
            "data": {
                "hour": {
                    "start_dat": str(agg_hour.start_dat),
                    "duration_sum": agg_hour.duration_sum,
                    "duration_max": agg_hour.duration_max,
                    "data": json.loads(JsonPlus().dumps(agg_hour.j)),
                },
                # JsonPlus.dumps(AggHour.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()),
                # "day": JsonPlus.dumps(AggDay.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()),
                "day": {
                    "start_dat": str(agg_day.start_dat),
                    "duration_sum": agg_day.duration_sum,
                    "duration_max": agg_day.duration_max,
                    "data": json.loads(JsonPlus().dumps(agg_day.j)),
                },
                # "month": JsonPlus.dumps(AggMonth.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()),
                # "year": JsonPlus.dumps(AggYear.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()),
                "month": {
                    "start_dat": str(agg_month.start_dat),
                    "duration_sum": agg_month.duration_sum,
                    "duration_max": agg_month.duration_max,
                    "data": json.loads(JsonPlus().dumps(agg_month.j)),
                },
                # "all": JsonPlus.dumps(AggAll.objects.filter(poste_id=mon_poste_id).order_by('-start_dat').first()),
                "year": {
                    "start_dat": str(agg_year.start_dat),
                    "duration_sum": agg_year.duration_sum,
                    "duration_max": agg_year.duration_max,
                    "data": json.loads(JsonPlus().dumps(agg_year.j)),
                },
                "all": {
                    "start_dat": str(agg_all.start_dat),
                    "duration_sum": agg_all.duration_sum,
                    "duration_max": agg_all.duration_max,
                    "data": json.loads(JsonPlus().dumps(agg_all.j)),
                },
            }
        }
        return ret_json

    except Exception as inst:
        return HttpResponse(inst)
