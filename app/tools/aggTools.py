import datetime
import calendar
import json
import math


def getAggLevels(is_tmp: bool = None):
    """
    getAggLevels
        return an array of aggregation levels

    Parameter:
        is_tmp
    """
    return ["H", "D", "M", "Y", "A"]


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


def getAggDuration(niveau_agg: str, start_dat: datetime) -> int:
    """get the aggregation (in minutes) depending on the level"""
    if niveau_agg == "H" or niveau_agg == "HT":
        return 60
    elif niveau_agg == "D" or niveau_agg == "DT":
        return 1440
    elif niveau_agg == "M" or niveau_agg == "MT":
        return int(calendar.monthrange(start_dat.year, start_dat.month)[1]) * 1440
    elif niveau_agg == "Y" or niveau_agg == "YT":
        if calendar.isleap(start_dat.year):
            return 366 * 1440
        return 365 * 1440
    elif niveau_agg == "A" or niveau_agg == "AT":
        # 100 years max...
        return 525600 * 100
    else:
        raise Exception("get_agg_duration", "wrong niveau_agg: " + niveau_agg)


def calcAggDateNextLevel(
    niveau_agg: str,
    start_dt_utc: datetime,
    factor: float = 0,
    is_stop_dat: bool = False,
) -> datetime:
    """
    Return the aggregation date of the next level, None when it's done
    """
    if niveau_agg == "H":
        next_niveau = "D"
    elif niveau_agg == "D":
        next_niveau = "M"
    elif niveau_agg == "M":
        next_niveau = "Y"
    elif niveau_agg == "Y":
        next_niveau = "A"
    else:
        return None
    return calcAggDate(next_niveau, start_dt_utc, factor, is_stop_dat)


def calcAggDate(
    niveau_agg: str,
    start_dt_utc_given: datetime,
    factor: float = 0,
    is_stop_dat: bool = False,
) -> datetime:
    """
    calc_agg_date
        returns the start of the datetime of the aggregation level

    Parameters:
        niveau_agg: H, HT, D, DT, M, MT, Y, YT, A, AT
        start_dt_utc: start date (is_stop_dat = False), stop_dat (is_stop_dat = True)
        factor: deca hour
        is_stop_dat: flag to determine if is is a start or a stop date
    """
    # start_dt_utc
    start_dt_utc = datetime.datetime(start_dt_utc_given.year, start_dt_utc_given.month, start_dt_utc_given.day, start_dt_utc_given.hour, 0, 0, 0)

    if is_stop_dat:
        if start_dt_utc_given.minute == 0 and start_dt_utc_given.second == 0:
            start_dt_utc = start_dt_utc - datetime.timedelta(hours=1)
        start_dt_utc = datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, start_dt_utc.hour, 0, 0, 0)
        start_dt_utc += datetime.timedelta(minutes=int(60 * factor))

    if niveau_agg[0] == "H":
        return start_dt_utc
    if niveau_agg[0] == "D":
        return datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, 0, 0, 0, 0)
    if niveau_agg[0] == "M":
        return datetime.datetime(start_dt_utc.year, start_dt_utc.month, 1, 0, 0, 0, 0)
    if niveau_agg[0] == "Y":
        return datetime.datetime(start_dt_utc.year, 1, 1, 0, 0, 0, 0)
    if niveau_agg[0] == "A":
        return datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    raise Exception("calc_period_date", "wrong niveau_agg: " + niveau_agg)


def isFlagged(bit_field: int, bit_to_check: int) -> bool:
    """
    isFlagged
        check if the bit is set

    Parameter:
        bit_field: bits field
        bit_to_check: bit to check
    """
    return (bit_field & int(bit_to_check)) == int(bit_to_check)


def addJson(j: json, key: str, valeur: int):
    """
    addJson

        add a value to j[key]

    Parameter:
        j: json field
        key: key to add
        valeur: value to add
    """
    if j.__contains__(key) is False:
        j[key] = 0
    j[key] += valeur


def shouldNullify(exclusion: json, src_key: str) -> bool:
    """
    shouldNullify
        Check if the exclusion requires to nullify the measure

    Parameter:
        exclusion: json coming from exclusion table
        src_key: key to check in the exclusion field
    """
    if exclusion is not None:
        if (exclusion.__contains__(src_key) is True and exclusion[src_key] == "null") or exclusion.__contains__(src_key) is False:
            return True
    return False


def loadFromExclu(exclusion, src_key: str) -> bool:
    """
    loadFromExclu
        check if the value should be loaded from the exclusion, not from the measured valued

    Parameter:
        exclusion: json coming from exclusion table
        src_key: key to check
    """
    if exclusion is not None and exclusion.__contains__(src_key) is True:
        if exclusion[src_key] != "null" and exclusion[src_key] != "value":
            return True
    return False


def delKey(j: json, key: str):
    """
    delKey
        delete a key in json if exists

    Parameter:
        j: json data
        key: key to delete if exists
    """
    if j.__contains__(key):
        del j[key]


def addNewAngle(angle, ang_nb=0, ang_sin=0, ang_cos=0):
    ''' addNewAngle : add new angle to average (from https://en.wikipedia.org/wiki/Circular_mean) '''
    angle = math.radians(angle)

    # print('before => si: ' + str(ang_sin) + ', co:  ' + str(ang_cos) + ', nb: ' + str(ang_nb) + ' -> mean: ' + str(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    # print('adding => si: ' + str(math.sin(angle)) + ', co:  ' + str(math.cos(angle)))
    ang_sin += math.sin(angle)
    ang_cos += math.cos(angle)
    ang_nb += 1
    # print('after  => si: ' + str(ang_sin) + ', co:  ' + str(ang_cos) + ', nb: ' + str(ang_nb) + ' -> mean: ' + str(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    return ang_nb, round(ang_sin, 3), round(ang_cos, 3)


def removeAngle(angle, ang_nb=0, ang_sin=0, ang_cos=0):
    ''' RemoveAngle : remove one angle to average (from https://en.wikipedia.org/wiki/Circular_mean) '''
    if ang_nb < 1:
        return 0, 0

    angle = math.radians(angle)

    # print('before => si: ' + str(ang_sin) + ', co:  ' + str(ang_cos) + ', nb: ' + str(ang_nb) + ' -> mean: ' + str(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    # print('adding => si: ' + str(math.sin(angle)) + ', co:  ' + str(math.cos(angle)))
    ang_sin -= math.sin(angle)
    ang_cos -= math.cos(angle)
    # print('after  => si: ' + str(ang_sin) + ', co:  ' + str(ang_cos) + ', nb: ' + str(ang_nb) + ' -> mean: ' + str(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    return round(ang_sin, 3), round(ang_cos, 3)


def getMeanAngle(ang_nb, ang_sin, ang_cos):
    ''' getMeanAngle: get average wind direction (from https://en.wikipedia.org/wiki/Circular_mean)'''
    if ang_nb == 0:
        return None
    ang_mean = math.atan2(ang_sin/ang_nb, ang_cos/ang_nb)
    ang_mean = math.degrees(ang_mean)
    if ang_mean < 0:
        ang_mean = 360 + ang_mean
    return round(ang_mean)


def updateWindData(j_data, key, value):
    if value is None:
        return
    k = key + '_dir'
    if j_data.get(k + '_nb') is None or j_data.get(k + '_sin') is None or j_data.get(k + '_cos') is None:
        j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'] = addNewAngle(value)
    else:
        j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'] = addNewAngle(value, j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'])
    j_data[k] = getMeanAngle(j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'])
