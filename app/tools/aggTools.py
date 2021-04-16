import json
import datetime
import dateutil.parser


def getAggLevels(is_tmp: bool = None):
    """ return aggregation levels for our computation """
    if is_tmp is None:
        raise Exception('getAggLevel', 'is_tmp not given')
    if is_tmp is False:
        return ['H', 'D', 'M', 'Y', 'A']
    return['HT', 'DT', 'MT', 'YT', 'AT']


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
    if niveau_agg == "H" or niveau_agg == "HT":
        return 60
    elif niveau_agg == "D" or niveau_agg == "DT":
        return 1440
    elif niveau_agg == "M" or niveau_agg == "MT":
        return 43920   # int(30.5 * 24 * 60)
    elif niveau_agg == "Y" or niveau_agg == "YT":
        return 525960    # int(365.25 * 24 * 60)
    elif niveau_agg == "A" or niveau_agg == "AT":
        raise Exception("get_gg_duration", "global has no duration")
    else:
        raise Exception("get_agg_duration", "wrong niveau_agg: " + niveau_agg)


def calcAggDateNextLevel(niveau_agg: str, start_dt_utc: datetime, factor: float = 0, is_measure_date: bool = False) -> datetime:
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
    elif niveau_agg == 'HT':
        next_niveau = 'DT'
    elif niveau_agg == 'DT':
        next_niveau = 'MT'
    elif niveau_agg == 'MT':
        next_niveau = 'YT'
    elif niveau_agg == 'YT':
        next_niveau = 'AT'
    else:
        return None
    return calcAggDate(next_niveau, start_dt_utc, factor, is_measure_date)


def fixUtcDate(my_date: datetime) -> datetime:
    tmp_dt1 = my_date.isoformat().replace('+00:00', '+04:00')
    return dateutil.parser.parse(tmp_dt1)


def calcAggDate(niveau_agg: str, start_dt_utc: datetime, factor: float = 0, is_measure_date: bool = False) -> datetime:
    """
        calc_agg_date

        returns the start of the datetime of the aggregation level
    """
    if niveau_agg == "H" or niveau_agg == 'HT':
        # if is_measure_date is True:
        #     delta_dt = datetime.timedelta(minutes=int(60 * (factor + ComputationParam.AddHourToMeasureInAggHour)))
        # else:
        delta_dt = datetime.timedelta(minutes=int(60 * factor))
        if is_measure_date and start_dt_utc.minute == 0 and start_dt_utc.second == 0:
            start_dt_utc = start_dt_utc - datetime.timedelta(hours=1)
        return fixUtcDate(datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, start_dt_utc.hour, 0, 0, 0, datetime.timezone.utc) + delta_dt)

    if niveau_agg == "D" or niveau_agg == 'DT':
        delta_dt = datetime.timedelta(minutes=int(60 * factor))
        if is_measure_date and start_dt_utc.minute == 0 and start_dt_utc.second == 0:
            start_dt_utc = start_dt_utc - datetime.timedelta(hours=1)
        if delta_dt != 0:
            start_dt_utc = start_dt_utc + delta_dt
        return fixUtcDate(datetime.datetime(start_dt_utc.year, start_dt_utc.month, start_dt_utc.day, 0, 0, 0, 0, datetime.timezone.utc))
    elif niveau_agg == "M" or niveau_agg == 'MT':
        delta_dt = datetime.timedelta(minutes=int(60 * factor))
        if is_measure_date and start_dt_utc.minute == 0 and start_dt_utc.second == 0:
            start_dt_utc = start_dt_utc - datetime.timedelta(hours=1)
        if delta_dt != 0:
            start_dt_utc = start_dt_utc + delta_dt
        return fixUtcDate(datetime.datetime(start_dt_utc.year, start_dt_utc.month, 1, 0, 0, 0, 0, datetime.timezone.utc))

    elif niveau_agg == "Y" or niveau_agg == 'YT':
        delta_dt = datetime.timedelta(minutes=int(60 * factor))
        if is_measure_date and start_dt_utc.minute == 0 and start_dt_utc.second == 0:
            start_dt_utc = start_dt_utc - datetime.timedelta(hours=1)
        if delta_dt != 0:
            start_dt_utc = start_dt_utc + delta_dt
        return fixUtcDate(datetime.datetime(start_dt_utc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc))

    elif niveau_agg == "A" or niveau_agg == 'AT':
        return fixUtcDate(datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc))

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
