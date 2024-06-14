import math


def addNewAngle(angle, ang_nb=0, ang_sin=0, ang_cos=0):
    ''' addNewAngle : add new angle to average (from https://en.wikipedia.org/wiki/Circular_mean) '''
    angle = math.radians(angle)

    # print('before => si: ' + '{0}'.format(ang_sin) + ', co:  ' + '{0}'.format(ang_cos) + ', nb: ' + '{0}'.format(ang_nb) + ' -> mean: ' + '{0}'.format(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    # print('adding => si: ' + '{0}'.format(math.sin(angle)) + ', co:  ' + '{0}'.format(math.cos(angle)))
    ang_sin += math.sin(angle)
    ang_cos += math.cos(angle)
    ang_nb += 1
    # print('after  => si: ' + '{0}'.format(ang_sin) + ', co:  ' + '{0}'.format(ang_cos) + ', nb: ' + '{0}'.format(ang_nb) + ' -> mean: ' + '{0}'.format(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    return ang_nb, round(ang_sin, 3), round(ang_cos, 3)


def removeAngle(angle, ang_nb=0, ang_sin=0, ang_cos=0):
    ''' RemoveAngle : remove one angle to average (from https://en.wikipedia.org/wiki/Circular_mean) '''
    if ang_nb < 1:
        return 0, 0

    angle = math.radians(angle)

    # print('before => si: ' + '{0}'.format(ang_sin) + ', co:  ' + '{0}'.format(ang_cos) + ', nb: ' + '{0}'.format(ang_nb) + ' -> mean: ' + '{0}'.format(getMeanAngle(ang_nb, ang_sin, ang_cos)))
    # print('adding => si: ' + '{0}'.format(math.sin(angle)) + ', co:  ' + '{0}'.format(math.cos(angle)))
    ang_sin -= math.sin(angle)
    ang_cos -= math.cos(angle)
    # print('after  => si: ' + '{0}'.format(ang_sin) + ', co:  ' + '{0}'.format(ang_cos) + ', nb: ' + '{0}'.format(ang_nb) + ' -> mean: ' + '{0}'.format(getMeanAngle(ang_nb, ang_sin, ang_cos)))
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
