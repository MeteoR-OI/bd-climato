import datetime
import calendar
import json
import math


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


# def updateWindData(j_data, key, value):
#     if value is None:
#         return
#     k = key + '_dir'
#     if j_data.get(k + '_nb') is None or j_data.get(k + '_sin') is None or j_data.get(k + '_cos') is None:
#         j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'] = addNewAngle(value)
#     else:
#         j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'] = addNewAngle(value, j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'])
#     j_data[k] = getMeanAngle(j_data[k + '_nb'], j_data[k + '_sin'], j_data[k + '_cos'])
