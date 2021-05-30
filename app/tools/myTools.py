from .jsonPlus import JsonPlus, json
from app.tools.telemetry import Span
from django.conf import settings
import datetime
import inspect
import logging


def LogCritical(e, my_span=None, params: json = {}, return_string: bool = False, stack_level: int = 0):
    """
        Log Exception

        Parameters:
            Exception
            span, or None
            parameters in a json variable
            return_string: True -> return the error message, else output the message
            stack_level: number of level to remove from the stack analysis
    """
    stack_level += 1
    if e.__dict__.__len__() > 0 and 'info' in e.__dict__:
        filenames = e.info["f"].split("/")
        if filenames.__len__() == 0:
            filenames = ["??"]
        filename = filenames[filenames.__len__() - 1]
        return LogMe.GetInstance().LogMeOutput(filename, e.info["l"], e.info["n"],  e.info["i"], 'error', my_span, params, return_string)
    else:
        e_str = str(e.__class__) + ':' + str(e)
    return LogMe.GetInstance().LogMe(e_str, "critical", my_span, params, stack_level, return_string)


def LogError(
    message: str, my_span=None, params: json = {}, return_string: bool = False
):
    return LogMe.GetInstance().LogMe(message, "error", my_span, params, 1, return_string)


def logWarning(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return LogMe.GetInstance().LogMe(message, "warning", my_span, params, 1, return_string)


def logInfo(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return LogMe.GetInstance().LogMe(message, "info", my_span, params, 1, return_string)


def LogDebug(
    message: str, my_span=None, params: json = {}, return_string: bool = False
):
    return LogMe.GetInstance().LogMe(message, "trace", my_span, params, 1, return_string)


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

        if self.prod is True:
            if self.debug is True:
                self.log = logging.getLogger('logDebugFile')
            else:
                self.log = logging.getLogger('logInfoFile')
        else:
            if self.debug is True:
                self.log = logging.getLogger('logDebugConsole')
            else:
                self.log = logging.getLogger('logInfoConsole')

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
        my_span: Span = None,
        params: json = {},
        stack_level: int = 0,
        return_string: bool = False,
    ):
        """centralized log output function"""
        stack_level += 1

        if level.lower() not in ["debug", "info", "warning", "error", "critical"]:
            level = "info"

        filename, line_no, module, stack_info = self.GetStackInfo(level, stack_level)
        if stack_info.__len__() > 0:
            params['stack'] = stack_info
        return self.LogMeOutput(filename, line_no, module, message, level, my_span, params, return_string)

    def LogMeOutput(
        self,
        filename: str,
        line_no: int,
        module: str,
        message: str,
        level: str = None,
        my_span: Span = None,
        params: json = {},
        return_string: bool = False,
    ):
        # build our json
        log_j = {
            "timestamp": str(datetime.datetime.now()),
            "pyFile": filename,
            "pyLine": line_no,
            "pyFunc": module,
            "level": level,
            "msg": self.CleanUpMessage(message),
            "params": params,
        }

        # add traceID
        if my_span is not None and my_span.get_span_context().trace_id is not None:
            log_j["trace_id"] = format(int(my_span.get_span_context().trace_id), 'x')
        else:
            log_j["trace_id"] = "no_trace"

        if hasattr(settings, "TELEMETRY") is True and settings.TELEMETRY is True:
            if return_string:
                return log_j
            msg = JsonPlus().dumps(log_j)
        else:
            msg = 'timestamp=' + str(log_j.get("timestamp")) + " "
            msg += 'level=' + str(log_j.get("level")).upper() + " "
            msg = ' pyFile=' + str(log_j.get("pyFile")) + " "
            msg += ' pyLine=' + str(log_j.get("pyLine"))
            msg += ' pyFunc=' + str(log_j.get("pyFunc"))
            msg += ' msg=' + str(log_j.get("msg")) + ' '
            if log_j.get("trace_id") != "no_trace" and log_j.get("trace_id") is not None:
                msg += 'traceID=' + str(log_j.get("trace_id")) + ' '
            if log_j.get("params") != {} and log_j.get("params") is not None:
                msg += ' params=' + JsonPlus().dumps(params) + ' '
            if return_string:
                return msg

        if level == 'debug':
            self.log.debug(msg)
        elif level == 'info':
            self.log.info(msg)
        elif level == 'warning':
            self.log.warning(msg)
        elif level == 'error':
            self.log.error(msg)
        elif level == 'critical':
            self.log.critical(msg)
        else:
            self.log.critical('Unknow level - ' + msg)

    def GetStackInfo(self, level: str, stack_level: int = 1):
        stack_formatted = []
        loc_caller = "??"
        loc_filename = "??"
        loc_module = "??"
        loc_line_no = 0
        idx_up = stack_level + 1
        idx = 0
        full_stack = inspect.stack()
        for a_stack_line in full_stack:
            if idx >= idx_up:
                filenames = a_stack_line.filename.split("/")
                if filenames.__len__() == 0:
                    filenames = ["??"]
                filename = filenames[filenames.__len__() - 1]
                caller = a_stack_line.function
                line_no = a_stack_line.lineno

                if idx == idx_up:
                    loc_filename = filename
                    loc_module = caller
                    loc_line_no = line_no
                if level in ["error"]:
                    stack_formatted.append(
                        filename + '--' + loc_caller + '::' + str(loc_line_no) + " -> " + str(a_stack_line.code_context)
                    )
                else:
                    break
            idx += 1

        return loc_filename, loc_line_no, loc_module, stack_formatted

    def CleanUpMessage(self, msg: str) -> str:
        """
            Clean up exception error message
        """
        if msg.startswith('ConnectionError(MaxRetryError("HTTPConnectionPool('):
            return "Connection Error, server probably not on-line or not accessible"
        return msg
