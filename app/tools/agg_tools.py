from app.models import Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global   #
from app.tools.climConstant import AggLevel
# import json
# import sys
import datetime
from dateutil.relativedelta import relativedelta


def convert_relative_hour(mesure_dt: datetime, hour_deca: int):
    """
        convert_relative_hour

        retourne le numero de l'heure relative pour une certaine mesure
        hour_deca est une propriete de la mesure

        le numero est negatif pour le jour precedent.
        le numero est > 24 pour le jour suivant
    """

    tmp_hour = mesure_dt.datetime.hour + hour_deca
    if tmp_hour >= 0:
        return tmp_hour

    # retoune le no de l'heure en negatif
    if tmp_hour < -24:
        raise Exception("convert_relative_hour", "tmp_hour:" + str(tmp_hour))
    return -24 - tmp_hour


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
            raise Exception("get_agg_object",
                            "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,


def calc_agg_date(niveau_agg: AggLevel, dt_utc: datetime, factor: float = 0) -> datetime:
    """
        calc_agg_date

        returns the start of the datetime of the aggregation level
        can return an datetime for half period (force=0.5)
    """
    try:
        if niveau_agg == "H":
            return datetime.datetime(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(minutes=int(60 * factor))

        if niveau_agg == "D":
            if int(factor) == 1:
                return datetime.datetime(dt_utc.year, dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(days=1)
            return datetime.datetime(dt_utc.year, dt_utc.month, dt_utc.day, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(hours=int(24 * factor))
        elif niveau_agg == "M":
            if int(factor) == 1:
                return datetime.datetime(dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=1)
            return datetime.datetime(dt_utc.year, dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(days=int(30.5 * factor))
        elif niveau_agg == "Y":
            if int(factor) == 1:
                return datetime.datetime(dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(years=1)
            return datetime.datetime(dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=int(12 * factor))
        elif niveau_agg == "A":
            return datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
        else:
            raise Exception("calc_period_date", "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,


def is_flagged(flag: int, setting: int) -> bool:
    """ check if the bit is set """
    return ((flag & int(setting)) == int(setting))
