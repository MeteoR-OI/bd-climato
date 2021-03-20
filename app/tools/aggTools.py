from app.tools.climConstant import AggLevel, ComputationParam
import json
import datetime
from dateutil.relativedelta import relativedelta


def convertRelativeHour(mesure_dt: datetime, hour_deca: int):
    """
        convert_relative_hour

        retourne le numero de l'heure relative pour une certaine mesure
        hour_deca est une propriete de la mesure

        le numero est negatif pour le jour precedent.
        le numero est > 24 pour le jour suivant
    """

    tmp_hour = mesure_dt.hour + hour_deca
    if tmp_hour >= 0:
        return tmp_hour

    # retoune le no de l'heure en negatif
    if tmp_hour < -24:
        raise Exception("convert_relative_hour", "tmp_hour:" + str(tmp_hour))
    return -24 - tmp_hour


def getRightAggregation(agg_niveau: str, start_dt_utc: datetime, hour_deca: int, aggregations: list):
    """
        getRightAggregation

        return the right aggregation, depending on the hour_deca
    """
    if agg_niveau != "D" or hour_deca != 0:
        return aggregations[0]

    # get relative hour
    hour_rel = convertRelativeHour(start_dt_utc, hour_deca)
    if hour_rel < 0:
        return aggregations[1]
    if hour_rel >= 24:
        return aggregations[2]
    return aggregations[0]


def getAggDuration(niveau_agg: str) -> int:
    """get the aggregation (in sec) depending on the level"""
    try:
        if niveau_agg == "H":
            return 60
        elif niveau_agg == "D":
            return 1440
        elif niveau_agg == "M":
            return 43920   # int(30.5 * 24 * 60)
        elif niveau_agg == "Y":
            return 525960    # int(365.25 * 24 * 60)
        elif niveau_agg == "A":
            raise Exception("get_gg_duration", "global has no duration")
        else:
            raise Exception("get_agg_duration", "wrong niveau_agg: " + niveau_agg)

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,


def calcAggDateNextLevel(niveau_agg: AggLevel, start_dt_utc: datetime, factor: float = 0) -> datetime:
    """
        Return the aggregation date of the next level, None when it's done
    """
    if niveau_agg == 'H':
        next_niveau = 'D'
    elif niveau_agg == 'D':
        next_niveau = 'M'
    elif niveau_agg == 'M':
        next_niveau = 'Y'
    elif niveau_agg == 'Y':
        next_niveau = 'A'
    else:
        return None
    return calcAggDate(next_niveau, start_dt_utc, factor)


def calcAggDate(niveau_agg: AggLevel, start_dt_utc: datetime, factor: float = 0) -> datetime:
    """
        calc_agg_date

        returns the start of the datetime of the aggregation level
    """
    if niveau_agg == "H":
        delta_dt = datetime.timedelta(minutes=int(60 * (factor + ComputationParam.AddHourToMeasureInAggHour)))
        return datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, start_dt_utc.hour, 0, 0, 0, datetime.timezone.utc) + delta_dt

    if niveau_agg == "D":
        if int(factor) == 1:
            return datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(days=1)
        if int(factor) == -1:
            return datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(days=-1)
        return datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(hours=int(24 * factor))

    elif niveau_agg == "M":
        if int(factor) == 1:
            return datetime.datetime(start_dt_utc.year, start_dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=1)
        if int(factor) == -1:
            return datetime.datetime(start_dt_utc.year, start_dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=-1)
        return datetime.datetime(start_dt_utc.year, start_dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(days=int(30.5 * factor))

    elif niveau_agg == "Y":
        if int(factor) == 1:
            return datetime.datetime(start_dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(years=1)
        if int(factor) == -1:
            return datetime.datetime(start_dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(years=-1)
        return datetime.datetime(start_dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=int(12 * factor))

    elif niveau_agg == "A":
        return datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    else:
        raise Exception("calc_period_date", "wrong niveau_agg: " + niveau_agg)


def isFlagged(flag: int, setting: int) -> bool:
    """ check if the bit is set """
    return ((flag & int(setting)) == int(setting))


def addJson(j: json, key: str, valeur):
    """
        addJson

        add the value to j[key]
    """
    if j.__contains__(key) is False:
        j[key] = 0
    j[key] += valeur


def shouldNullify(exclusion: json, src_key: str) -> bool:
    # Check if the exclusion requires to nullify the measure
    if exclusion is not None:
        if (exclusion.__contains__(src_key) is True and exclusion[src_key] == 'null') or exclusion.__contains__(src_key) is False:
            return True
    return False


def loadFromExclu(exclusion, src_key: str) -> bool:
    # check if the value should be loaded from the exclusion, not from the measured valued
    if exclusion is not None and exclusion.__contains__(src_key) is True:
        if exclusion[src_key] != 'null' and exclusion[src_key] != 'value':
            return True
    return False


def delKey(j: json, key: str):
    # delete a key in json if exists
    if j.__contains__(key):
        del j[key]
