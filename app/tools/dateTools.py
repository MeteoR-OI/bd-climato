import datetime
import dateutil.parser
import sys


def date_to_str(my_date: datetime.datetime) -> str:
    """
    date_to_str
        convert date to string, without timezone information

    Parameters:
        datetime data
    """
    try:
        if isinstance(my_date, str) is True:
            tmp_str = my_date
        else:
            tmp_str = my_date.isoformat()
        if tmp_str.find("+") > -1:
            tmp_str = tmp_str[:tmp_str.find("+")]
        return tmp_str
    except Exception as e:
        if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            exception_info = e.__repr__()
            filename = exception_traceback.tb_frame.f_code.co_filename
            funcname = exception_traceback.tb_frame.f_code.co_name
            line_number = exception_traceback.tb_lineno
            e.info = {
                "i": str(exception_info),
                "n": funcname,
                "f": filename,
                "l": line_number,
            }
            e.done = True
        raise e


def str_to_date(dt_str: str) -> datetime.datetime:
    """
    str_to_date
        convert string to datetime

    Parameters:
        string data, format: "YYYY-MM-DDThh:mm:ss"
    """
    try:
        if isinstance(dt_str, datetime.datetime) is True:
            return dt_str
        if isinstance(dt_str, str) is False:
            raise Exception('str_to_date', 'bad param, type: ' + str(type(dt_str)))
        if dt_str.find("+") > -1:
            dt_str = dt_str[:dt_str.find("+")]
        return dateutil.parser.parse(dt_str + '+04:00')
    except Exception as e:
        if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            exception_info = e.__repr__()
            filename = exception_traceback.tb_frame.f_code.co_filename
            funcname = exception_traceback.tb_frame.f_code.co_name
            line_number = exception_traceback.tb_lineno
            e.info = {
                "i": str(exception_info),
                "n": funcname,
                "f": filename,
                "l": line_number,
            }
            e.done = True
        raise e
