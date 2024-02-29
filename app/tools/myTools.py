from app.classes.repository.incidentMeteor import IncidentMeteor
from django.conf import settings
import traceback
import datetime
import inspect
import logging
import json

# logException(e, params):
# logCritical(source, message: str, params):


def notifyAdmin(type, message: str, params: json = {}, create_info_log: bool = True):
    print("notifyAdmin:", type + ' =>', message, params)
    if create_info_log is True:
        return LogMe.GetInstance().LogMe(message, "info", params)


def logException(e, params: json = {}):
    message, params['stack'] = get_trace_info(e)
    stack_0 = params['stack'].split('\n')[0]
    msg_line = stack_0.split(' ')
    filenames = msg_line[3][:-1].split("/")
    if filenames.__len__() == 0:
        filenames = ["??"]
    filename = filenames[filenames.__len__() - 1]
    line_no = msg_line[5][:-1]
    module = msg_line[7]
    params['code'] = params['stack'].split('\n')[1]
    IncidentMeteor.new(
        'exception',
        'critical',
        message.split(':')[1],
        params,
    )
    notifyAdmin('exception', message.split(':')[1], params, False)
    # filename, line_no, module = self.GetStackInfo(5 if level == "critical" else 2)
    return LogMe.GetInstance().LogMeOut(filename, line_no, module, message.split(':')[1], 'critical', params)
    # return LogMe.GetInstance().LogMe(message, "critical", params)


def logError(source, message: str, params: json = {}):
    IncidentMeteor.new(
        source,
        'error',
        message,
        params,
    )
    notifyAdmin('error', message, params, False)

    return LogMe.GetInstance().LogMe(message, "error", params)


def logInfo(message: str, params: json = {}):
    return LogMe.GetInstance().LogMe(message, "info", params)


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


def GetFirstDayNextMonthFromTs(ts, delta_hours=0):
    # Convert to local date
    dt_local = FromTimestampToDateTime(int(ts), delta_hours)
    # return first day next month in local timezone
    return datetime.datetime(dt_local.year + (dt_local.month // 12), (dt_local.month % 12) + 1, 1, 0, 0, 0, 0) - datetime.timedelta(hours=delta_hours)


def FromTimestampToDateTime(ts, delta_hours=0):
    """Load a timestamp to a datetime, as local time, or utc time (no tz given)"""
    return datetime.datetime.fromtimestamp(ts + delta_hours * 3600).replace(tzinfo=None)


def AsTimezone(dt, delta_hours=0):
    if type(dt) is datetime.date:
        return dt
    return dt + datetime.timedelta(hours=delta_hours)


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
        params: json = {}
    ):
        """
            LogMe

            get filename, line_no module from current stack
        """

        if level.lower() not in ["info", "error", "critical"]:
            level = "info"

        filename, line_no, module = self.GetStackInfo(5 if level == "critical" else 2)
        return self.LogMeOut(filename, line_no, module, message, level, params)

    def LogMeOut(
        self,
        filename: str,
        line_no: int,
        module: str,
        message: str,
        level: str = None,
        params: json = {},
    ):
        if level.lower() not in ["info", "error", "critical"]:
            level = "info"

        msg = 'timestamp=' + '"' + str(datetime.datetime.now()) + '" '
        msg += 'pyFile=' + filename + " "
        msg += 'pyLine=' + str(line_no) + " "
        msg += 'pyFunc=' + module + " "
        msg += 'msg="' + self.CleanUpMessage(message) + '" '
        if params != {}:
            for key in params:
                msg += key + '="' + str(params[key]) + '" '

        if level == 'info':
            self.log.info(msg)
        elif level == 'error':
            self.log.error(msg)
        elif level == 'critical':
            self.log.critical(msg)
        else:
            self.log.critical('Unknow level - ' + msg)

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
