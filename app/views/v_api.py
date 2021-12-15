#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse, HttpResponseBadRequest
from app.tools.jsonPlus import JsonPlus
# from django.conf import settings
# import os
station_list = ["BBF015", "MTG320"]


def view_stations_list(request):
    try:
        ret_json = station_list
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)


def view_stations_data(request, station: str = None):
    try:
        if station is None or station not in station_list:
            return HttpResponseBadRequest("no station given")
        ret_json = {
            "station": {
                "name": station,
                "info": "blabla",
            },
            "data": {
                "hour": {
                    "stop_dat": "2021-12-06 14:00+04:00",
                    "out_temp": 18,
                    "out_temp_max": 18,
                    "out_temp_max_time": "2021-12-06 12:37:53+04:00",
                    "out_temp_min": 15,
                    "out_temp_min_time": "2021-12-06 02:12:44+04:00",
                },
                "day": {
                    "stop_dat": "2021-12-06 14:00+04:00",
                    "out_temp": 18,
                    "out_temp_max": 18,
                    "out_temp_max_time": "2021-12-06 12:37:53+04:00",
                    "out_temp_min": 15,
                    "out_temp_min_time": "2021-12-06 02:12:44+04:00",
                },
                "month": {
                    "stop_dat": "2021-12-06 14:00+04:00",
                    "out_temp": 18,
                    "out_temp_max": 18,
                    "out_temp_max_time": "2021-12-06 12:37:53+04:00",
                    "out_temp_min": 15,
                    "out_temp_min_time": "2021-12-06 02:12:44+04:00",
                },
                "year": {
                    "stop_dat": "2021-12-06 14:00+04:00",
                    "out_temp": 18,
                    "out_temp_max": 18,
                    "out_temp_max_time": "2021-12-06 12:37:53+04:00",
                    "out_temp_min": 15,
                    "out_temp_min_time": "2021-12-06 02:12:44+04:00",
                },
                "all": {
                    "stop_dat": "2021-12-06 14:00+04:00",
                    "out_temp": 18,
                    "out_temp_max": 18,
                    "out_temp_max_time": "2021-12-06 12:37:53+04:00",
                    "out_temp_min": 15,
                    "out_temp_min_time": "2021-12-06 02:12:44+04:00",
                },
            }
        }
        ret = JsonPlus().dumps(ret_json)
        return HttpResponse(ret)

    except Exception as inst:
        return HttpResponse(inst)
