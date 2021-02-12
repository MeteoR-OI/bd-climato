from app.models import Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global   #
# import json
# import sys
import datetime


def round_datetime_per_aggregation(dt, niveau_agg):
    """arrondi la date, suivant le niveau d'agreggation"""
    try:
        if niveau_agg == "H":
            return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0, 0, datetime.timezone.utc)
        elif niveau_agg == "D":
            return datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, datetime.timezone.utc)
        elif niveau_agg == "M":
            return datetime.datetime(dt.year, dt.month, 1, 0, 0, 0, 0, datetime.timezone.utc)
        elif niveau_agg == "Y":
            return datetime.datetime(dt.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
        elif niveau_agg == "A":
            return datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
        else:
            raise Exception("round_datetime_per_aggregation", "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,


def get_agg_object(niveau_agg):
    """get the aggregation depending on the level"""
    try:
        if niveau_agg == "H":
            return Agg_hour
        elif niveau_agg == "D":
            return Agg_day
        elif niveau_agg == "M":
            return Agg_month
        elif niveau_agg == "Y":
            return Agg_year
        elif niveau_agg == "A":
            return Agg_global
        else:
            raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
