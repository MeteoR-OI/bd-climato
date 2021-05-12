from app.tools.telemetry import Span
from .jsonPlus import JsonPlus, json
from django.conf import settings
import datetime
import inspect


def LogException(inst, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(str(inst), 'error', my_span, params, 1, return_string)


def LogError(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(message, 'error', my_span, params, 1, return_string)


def logInfo(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(message, 'info', my_span, params, 1, return_string)


def logTrace(message: str, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(message, 'trace', my_span, params, 1, return_string)


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
            raise Exception('CopyJson', 'type michmatch on key: ' + str(k) + ' type: ' + str(type(dest[k])))
        CopyJson(src[k], dest[k])
        return

    if "'list'" in type_val:
        if dest.__contains__(k) is False:
            dest[k] = []
        elif str(type(dest[k])).index("'list'") is False:
            raise Exception('CopyJson', 'type michmatch on key: ' + str(k) + ' type: ' + str(type(dest[k])))
        CopyJson(src[k], dest[k])
        return
    dest[k] = v


def _logMe(message: str, level: str = None, my_span: Span = None, params: json = {}, stack_level: int = 0, return_string: bool = False):
    """ centralized log output function """
    stack_level += 1
    trace_id = None
    if my_span is not None:
        trace_id = my_span.get_span_context().trace_id

    if level.lower() not in ['info', '???', 'error', 'trace']:
        level = '??? ' + level

    location, stack_info = getStackInfo(level, stack_level)

    # build our json
    log_j = {
        "ts": datetime.datetime.now(),
        "loc": location,
        "msg": message
    }
    # add level
    log_j['level'] = level
    if stack_info.__len__() > 0:
        log_j['stack'] = stack_info
    # add trace_id
    if trace_id != 'no_trace_id':
        log_j['trace_id'] = trace_id
    # add our json Keys/Values
    for k, v in params.items():
        log_j[k] = v

    if return_string:
        return log_j

    if hasattr(settings, 'TELEMETRY') is True and settings.TELEMETRY is True:
        print(JsonPlus().dumps(log_j))
    else:
        if level == 'error':
            print('---------------------------------------------------------------------')
        print(
            str(log_j['ts']) + ' ' +
            log_j['loc'] + ' - ' +
            log_j['level'] + ' -> ' +
            log_j['msg'] + ' [' +
            str(log_j.get('trace_id')) + "] " +
            JsonPlus().dumps(params)
        )
        if log_j.get('stack') is not None:
            print('     ** stack **:')
            for a_line_stack in log_j['stack']:
                print(a_line_stack)
        if level == 'error':
            print('---------------------------------------------------------------------')


def getStackInfo(level: str, stack_level: int = 1):
    stack_formatted = []
    loc_caller = '??'
    idx_up = stack_level + 1
    idx = 0
    full_stack = inspect.stack()
    for a_stack_line in full_stack:
        if idx >= idx_up:
            filenames = a_stack_line.filename.split('/')
            if filenames.__len__() == 0:
                filenames = ['??']
            location = filenames[filenames.__len__() - 1] + '::' + a_stack_line.function + '::' + str(a_stack_line.lineno)
            if idx == idx_up:
                loc_caller = location
            if level in ['error']:
                stack_formatted.append(location + " -> " + str(a_stack_line.code_context))
            else:
                break
        idx += 1

    return loc_caller, stack_formatted
