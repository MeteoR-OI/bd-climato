import datetime
import dateutil.parser


def date_to_str(my_date: datetime.datetime) -> str:
    """
    date_to_str
        convert date to string, without timezone information

    Parameters:
        datetime data
    """
    if isinstance(my_date, str) is True:
        tmp_str = my_date
    else:
        tmp_str = my_date.isoformat()
    if tmp_str.find("+") > -1:
        tmp_str = tmp_str[:tmp_str.find("+")]
    return tmp_str


def str_to_datetime(dt_str: str) -> datetime.datetime:
    """
    str_to_date
        convert string to datetime

    Parameters:
        string data, format: "YYYY-MM-DDThh:mm:ss"
    """
    if isinstance(dt_str, datetime.datetime) is True:
        return dt_str
    if isinstance(dt_str, str) is False:
        raise Exception('str_to_date', 'bad param, type: ' + '{0}'.format(type(dt_str)))
    if dt_str.find("+") > -1:
        dt_str = dt_str[:dt_str.find("+")]
    tmp_dt = dateutil.parser.parse(dt_str)
    # tmp_dt.tzinfo = None
    return tmp_dt


def change_tz(dt: datetime.datetime, tz: int) -> datetime.datetime:
    """
    change_tz
        change timezone of a datetime

    Parameters:
        datetime data
        timezone string
    """
    if isinstance(dt, datetime.datetime) is False:
        raise Exception('change_tz', 'bad param, type: ' + '{0}'.format(type(dt)))
    if isinstance(tz, int) is False:
        raise Exception('change_tz', 'bad param, type: ' + '{0}'.format(type(tz)))
    return dt + datetime.timedelta(hours=tz)


def isRoundedHourInDuration(start_datetime, duration_seconds):
    if start_datetime == start_datetime.replace(minute=0, second=0, microsecond=0):
        end_datetime = start_datetime
    else:
        tmp_datetime = (start_datetime + datetime.timedelta(hours=1))
        end_datetime = tmp_datetime.replace(minute=0, second=0, microsecond=0)
    begin_datetime = end_datetime - datetime.timedelta(seconds=duration_seconds)
    # print('range: ' + '{0}'.format(begin_datetime) + ' to ' + '{0}'.format(end_datetime))
    # print("date " + '{0}'.format(start_datetime) + " before : " + '{0}'.format(start_datetime > begin_datetime))
    # print("date " + '{0}'.format(start_datetime) + " after : " + '{0}'.format(start_datetime <= end_datetime))
    return (start_datetime > begin_datetime) and (start_datetime <= end_datetime)

def FromTimestampToLocalDateTime(ts, delta_hours=0):
    """Load a timestamp to a datetime, as local time, or utc time (no tz given)"""
    return datetime.datetime.fromtimestamp(ts + delta_hours * 3600).replace(tzinfo=None)

def FromTimestampToUTCDateTime(ts):
    """Load a timestamp to a datetime, as local time, or utc time (no tz given)"""
    return datetime.datetime.fromtimestamp(ts).replace(tzinfo=None)

def GetFirstDayNextMonthFromTs(ts, delta_hours=0):
    # Convert to local date
    dt_local = FromTimestampToLocalDateTime(int(ts), delta_hours)
    # return first day next month in local timezone
    return datetime.datetime(dt_local.year + (dt_local.month // 12), (dt_local.month % 12) + 1, 1, 0, 0, 0, 0) - datetime.timedelta(hours=delta_hours)
