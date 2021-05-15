from app.tools.telemetry import Span
from .jsonPlus import JsonPlus, json
from django.conf import settings
import datetime
import inspect


def LogException(
    e, my_span=None, params: json = {}, return_string: bool = False, stack_level: int = 0
):
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
        return _logMeOutput(filename, e.info["l"], e.info["i"], 'error', my_span, params, return_string)
    else:
        e_str = str(e)
    return _logMe(e_str, "error", my_span, params, stack_level, return_string)


def LogError(
    message: str, my_span=None, params: json = {}, return_string: bool = False
):
    return _logMe(message, "error", my_span, params, 1, return_string)


def logInfo(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(message, "info", my_span, params, 1, return_string)


def logTrace(
    message: str, my_span=None, params: json = {}, return_string: bool = False
):
    return _logMe(message, "trace", my_span, params, 1, return_string)


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


def _logMe(
    message: str,
    level: str = None,
    my_span: Span = None,
    params: json = {},
    stack_level: int = 0,
    return_string: bool = False,
):
    """centralized log output function"""
    stack_level += 1

    if level.lower() not in ["info", "???", "error", "trace"]:
        level = "??? " + level

    filename, line_no, stack_info = getStackInfo(level, stack_level)
    if stack_info.__len__() > 0:
        params['stack'] = stack_info
    return _logMeOutput(filename, line_no, message, level, my_span, params, return_string)


def _logMeOutput(
    filename: str,
    line_no: int,
    message: str,
    level: str = None,
    my_span: Span = None,
    params: json = {},
    return_string: bool = False,
):
    # build our json
    log_j = {
        "ts": str(datetime.datetime.now()),
        "filename": filename,
        "line": line_no,
        "level": level,
        "msg": cleanUpMessage(message),
    }

    # add trace_id
    if my_span is not None:
        log_j["trace_id"] = my_span.get_span_context().trace_id
    else:
        log_j["trace_id"] = "no trace"

    # add our json Keys/Values
    for k, v in params.items():
        log_j[k] = v

    if return_string:
        return log_j

    if hasattr(settings, "TELEMETRY") is True and settings.TELEMETRY is True:
        print(JsonPlus().dumps(log_j))
    else:
        if level == "error":
            print(
                "---------------------------------------------------------------------"
            )
        print(
            str(log_j["ts"])
            + " " + str(log_j["level"]).upper()
            + " " + str(log_j["filename"])
            + " " + str(log_j["line"])
            + " -> " + log_j["msg"]
            + " [" + str(log_j["trace_id"]) + "] "
            + JsonPlus().dumps(params)
        )
        if log_j.get("stack") is not None:
            print("     ** stack **:")
            for a_line_stack in log_j["stack"]:
                print(a_line_stack)
        if level == "error":
            print(
                "---------------------------------------------------------------------"
            )


def getStackInfo(level: str, stack_level: int = 1):
    stack_formatted = []
    loc_caller = "??"
    loc_filename = "??"
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
                loc_filename = filename + '::' + caller
                loc_line_no = line_no
            if level in ["error"]:
                stack_formatted.append(
                    filename + '--' + loc_caller + '::' + str(loc_line_no) + " -> " + str(a_stack_line.code_context)
                )
            else:
                break
        idx += 1

    return loc_filename, loc_line_no, stack_formatted


def cleanUpMessage(msg: str) -> str:
    """
        Clean up exception error message
    """
    if msg.startswith('ConnectionError(MaxRetryError("HTTPConnectionPool('):
        return msg.split("):")[0].replace('(MaxRetryError', '')
    return msg
