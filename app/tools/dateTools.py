import datetime
import dateutil.parser


def date_to_str(my_date: datetime.datetime) -> str:
    # convert date to string, without timezone information
    if isinstance(my_date, str) is True:
        tmp_str = my_date
    else:
        tmp_str = my_date.isoformat()
    if tmp_str.find("+") > -1:
        tmp_str = tmp_str[:tmp_str.find("+")]
    return tmp_str


def str_to_date(dt_str: str) -> datetime.datetime:
    # convert string to datetime
    # current_tz = timezone.get_current_timezone()
    if isinstance(dt_str, datetime.datetime) is True:
        return dt_str
    if isinstance(dt_str, str) is False:
        raise Exception('str_to_date', 'bad param, type: ' + str(type(dt_str)))
    if dt_str.find("+") > -1:
        dt_str = dt_str[:dt_str.find("+")]
    return dateutil.parser.parse(dt_str + '+04:00')
