from app.models import Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global   #
# import json
# import sys
import datetime

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
            raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
