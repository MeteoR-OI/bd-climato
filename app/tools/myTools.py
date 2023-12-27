from app.classes.repository.incidentMeteor import IncidentMeteor
from app.tools.jsonPlus import JsonPlus
from django.conf import settings
import traceback
import datetime
import inspect
import logging
import json

# logException(e, my_span, params):
# logCritical(source, message: str, my_span, params):


def logException(e, my_span=None, params: json = {}):
    message, params['stack'] = get_trace_info(e)
    IncidentMeteor.new(
        'exception',
        'critical',
        message,
        params,
    )
    if my_span is not None:
        my_span.add_event('exception', str(e))
    return LogMe.GetInstance().LogMe(message, "critical", my_span, params)


def logCritical(source, message: str, my_span=None, params: json = {}):
    IncidentMeteor.new(
        source,
        'critical',
        'message',
        params,
    )
    if my_span is not None:
        my_span.add_event('critical', message)
    return LogMe.GetInstance().LogMe(message, "critical", my_span, params)


def logError(source, message: str, my_span=None, params: json = {}):
    IncidentMeteor.new(
        source,
        'error',
        'message',
        params,
    )
    if my_span is not None:
        my_span.add_attribute('error', message)
    return LogMe.GetInstance().LogMe(message, "error", my_span, params)


def logWarning(message: str, my_span=None, params: json = {}):
    if my_span is not None:
        my_span.add_attribute('warning', message)
    return LogMe.GetInstance().LogMe(message, "warning", my_span, params)


def logInfo(message: str, my_span=None, params: json = {}):
    return LogMe.GetInstance().LogMe(message, "info", my_span, params)


def CopyJson(src: json, dest: json):
    if "'list'" in str(type(src)):
        for one_src in src:
            type_val = str(type(one_src))
            if "'dict'" in type_val:
                new_array = {}
                dest.append(new_array)
                CopyJson(one_src, new_array)
            elif "'list'" in type_val:
                new_array = []
                dest.append(new_array)
                CopyJson(one_src, new_array)
            else:
                dest.append(one_src)
    else:
        for k, v in src.items():
            _copyJson(src, dest, k, v)


def _copyJson(src: json, dest: json, k: str, v):
    type_val = str(type(v))
    if "'dict'" in type_val:
        if dest.__contains__(k) is False:
            dest[k] = {}
        elif str(type(dest[k])).index("'dict'") is False:
            raise Exception(
                "CopyJson",
                "type michmatch on key: " + str(k) + " type: " + str(type(dest[k])),
            )
        CopyJson(src[k], dest[k])
        return

    if "'list'" in type_val:
        if dest.__contains__(k) is False:
            dest[k] = []
        elif str(type(dest[k])).index("'list'") is False:
            raise Exception(
                "CopyJson",
                "type michmatch on key: " + str(k) + " type: " + str(type(dest[k])),
            )
        CopyJson(src[k], dest[k])
        return
    dest[k] = v


def get_trace_info(exc, nb_levels: int = 3):
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(exc.__traceback__)  # add limit=??
    pretty = traceback.format_list(stack)
    stack = []
    idx_stack = pretty.__len__()
    idx_level = nb_levels
    while idx_level > 0 and idx_stack > 0:
        idx_level -= 1
        idx_stack -= 1
        stack.append(pretty[idx_stack])

    return str(exc.__class__) + ':' + str(exc), ''.join(stack)


def GetDate(dt):
    type_date = str(type(dt))
    if "'datetime.date'>" in type_date:
        return dt
    return dt.date()


def GetFirstDayNextMonth(dt, delta_hours=0):
    tz = datetime.timezone(datetime.timedelta(hours=delta_hours), 'UTC' + str('{:+03d}:00'.format(delta_hours)))
    if type(dt) is datetime.datetime:
        # Convert to local date
        dt_utc = AsTimezone(dt, delta_hours)
        # return first day next month in local timezone
        new_dt_utc = datetime.datetime(dt_utc.year + (dt_utc.month // 12), (dt_utc.month % 12) + 1, 1, tzinfo=tz)
        # Return an UTC datetime
        return AsTimezone(new_dt_utc, 0)
    # process for date type
    dt_utc = dt - datetime.timedelta(days=1)
    return datetime.datetime(dt_utc.year + (dt_utc.month // 12), (dt_utc.month % 12) + 1, 1, tzinfo=tz)


def FromTimestampToDate(ts, delta_hours=0):
    """Load a timestamp to a datetime, as local time, or utc time (no tz given)"""
    tz = datetime.timezone(datetime.timedelta(hours=delta_hours), 'UTC' + str('{:+03d}:00'.format(delta_hours)))
    return datetime.datetime.fromtimestamp(ts, tz)


def FromAwareDtToTimestamp(dt):
    """Return timestamp for an aware date (with no timezone data)"""
    return int(AsTimezone(dt).timestamp())


def AsTimezone(dt, delta_hours=0, no_tz=False):
    if type(dt) is datetime.date:
        return dt
    tz = datetime.timezone(datetime.timedelta(hours=delta_hours), 'UTC' + str('{:+03d}:00'.format(delta_hours)))
    if no_tz is False:
        return dt.astimezone(tz)
    return dt.astimezone(tz).replace(tzinfo=None)


def FromTsToLocalDateTime(ts, tz):
    tmp_dt = FromTimestampToDate(ts)
    return AsTimezone(tmp_dt, tz)


def FromDateToLocalDateTime(dt, delta_hours=0):
    tz = datetime.timezone(datetime.timedelta(hours=delta_hours), 'UTC' + str('{:+03d}:00'.format(delta_hours)))
    return datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, tzinfo=tz)


def RoundToStartOfDay(timestamp, delta_hours=0):
    tz = datetime.timezone(datetime.timedelta(hours=delta_hours), 'UTC' + str('{:+03d}:00'.format(delta_hours)))
    dt = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    dt = AsTimezone(dt, delta_hours)
    start_of_day = datetime.datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=tz)
    return int(start_of_day.timestamp())


def ToLocalTS(dt):
    """Return timestamp for a naive date (with no timezone data)"""
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())


def ToReunionTS(dt):
    """Return timestamp for a date in local time in UTC+4"""
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds() - 4 * 3600)


class LogMe:
    """
    LogMe
        Output Log Messages

        settings.py

        when used log files are stored in LOG_FILE_DIR/logInfo.log or LOG_FILE_DIR/logDebug.log

        TELEMETRY = True => output JSON on log files
        PROD=True => output std logging messages on log files
        PROD = False -> output
    """
    debug = False
    telemetry = False
    prod = False

    def __init__(self):
        # get our settings
        if hasattr(settings, "DEBUG") and settings.DEBUG is True:
            self.debug = True
        if hasattr(settings, "PROD") and settings.PROD is True:
            self.prod = True
        if hasattr(settings, "TELEMETRY") and settings.TELEMETRY is True:
            self.telemetry = True

        if self.prod is False or self.debug is True:
            self.log = logging.getLogger('log_dev')
        else:
            self.log = logging.getLogger('log_prod')

    @staticmethod
    def GetInstance():
        # return the instance
        if LogMe.__dict__.__contains__('my_instance') is False:
            LogMe.my_instance = LogMe()
        return LogMe.my_instance

    def LogMe(
        self,
        message: str,
        level: str = None,
        my_span=None,
        params: json = {}
    ):
        """
            LogMe

            get filename, line_no module from current stack
        """

        if level.lower() not in ["info", "warning", "error", "critical"]:
            level = "info"

        filename, line_no, module = self.GetStackInfo()
        return self.LogMeOutput(filename, line_no, module, message, level, my_span, params)

    def LogMeOutput(
        self,
        filename: str,
        line_no: int,
        module: str,
        message: str,
        level: str = None,
        my_span=None,
        params: json = {},
    ):
        # build our json
        log_j = {
            "timestamp": str(datetime.datetime.now()),
            "pyFile": filename,
            "pyLine": line_no,
            "pyFunc": module,
            "level": level,
            "msg": self.CleanUpMessage(message),
            # "params": params,
        }
        # add params values
        if params != {}:
            for key in params:
                log_j[key] = params[key]

        # add traceID
        if my_span is not None and my_span.get_span_context().trace_id is not None:
            log_j["traceID"] = format(int(my_span.get_span_context().trace_id), 'x')
            log_j["spanID"] = format(int(my_span.get_span_context().span_id), 'x')
        else:
            log_j["traceID"] = "no_trace"
            log_j["spanID"] = "no_trace"

        if hasattr(settings, "TELEMETRY") is True and settings.TELEMETRY is True:
            msg = JsonPlus().dumps(log_j)
        else:
            msg = 'timestamp=' + str(log_j.get("timestamp")) + " "
            msg += 'level=' + str(log_j.get("level")).upper() + " "
            msg += 'pyFile=' + str(log_j.get("pyFile")) + " "
            msg += 'pyLine=' + str(log_j.get("pyLine")) + " "
            msg += 'pyFunc=' + str(log_j.get("pyFunc")) + " "
            msg += 'msg="' + str(log_j.get("msg")) + '" '
            if log_j.get("traceID") != "no_trace" and log_j.get("traceID") is not None:
                msg += 'traceID=' + str(log_j.get("traceID")) + " "
            if log_j.get("spanID") != "no_trace" and log_j.get("spanID") is not None:
                msg += 'spanID=' + str(log_j.get("spanID")) + " "
            if params != {}:
                for key in params:
                    msg += "  " + key + "=" + str(params[key]) + " "

        if level == 'info':
            self.log.info(msg)
        elif level == 'warning':
            self.log.warning(msg)
        elif level == 'error':
            self.log.error(msg)
        elif level == 'critical':
            self.log.critical(msg)
        else:
            self.log.critical('Unknow level - ' + msg)

        return msg

    def GetStackInfo(self, stack_level: int = 0):
        loc_filename = "??"
        loc_module = "??"
        loc_line_no = 0
        idx_up = stack_level + 1
        idx = 0
        full_stack = inspect.stack()
        for a_stack_line in full_stack:
            if idx == idx_up:
                filenames = a_stack_line.filename.split("/")
                if filenames.__len__() == 0:
                    filenames = ["??"]
                loc_filename = filenames[filenames.__len__() - 1]
                loc_module = a_stack_line.function
                loc_line_no = a_stack_line.lineno
                break
            idx += 1

        return loc_filename, loc_line_no, loc_module

    def CleanUpMessage(self, msg: str) -> str:
        """
            Clean up exception error message
        """
        if repr(msg).startswith('ConnectionError(MaxRetryError("HTTPConnectionPool('):
            return "Connection Error, server probably not on-line or not accessible"
        return msg
