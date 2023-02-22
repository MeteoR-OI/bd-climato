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


def str_to_date(dt_str: str) -> datetime.datetime:
    """
    str_to_date
        convert string to datetime

    Parameters:
        string data, format: "YYYY-MM-DDThh:mm:ss"
    """
    if isinstance(dt_str, datetime.datetime) is True:
        return dt_str
    if isinstance(dt_str, str) is False:
        raise Exception('str_to_date', 'bad param, type: ' + str(type(dt_str)))
    if dt_str.find("+") > -1:
        dt_str = dt_str[:dt_str.find("+")]
    tmp_dt = dateutil.parser.parse(dt_str)
    # tmp_dt.tzinfo = None
    return tmp_dt
