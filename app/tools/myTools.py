from .jsonPlus import JsonPlus, json
import datetime
import inspect


def LogException(inst, my_span=None, params: json = {}, return_string: bool = False):
    return _logMe(str(inst), 'error', my_span, params, 1, return_string)


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
    # print(str(k) + ":" + str(v))
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


def _logMe(message: str, level: str = None, my_span=None, params: json = {}, stack_level: int = 0, return_string: bool = False):
    """ centralized log output function """
    span_id = None
    if my_span is not None:
        span_id = my_span.get_span_context().span_id

    stack_line = inspect.stack()[1 + stack_level]
    location = stack_line.function + '::' + str(stack_line.lineno)

    if level.lower() not in ['info', '???', 'error', 'trace']:
        level = '??? ' + level

    # build our json
    log_j = {
        "ts": datetime.datetime.now(),
        "loc": location,
        "msg": message
    }
    # add level
    if level is not None:
        log_j['level'] = level
    # add span_id
    if span_id is not None:
        log_j['span_id'] = span_id
    # add our json Keys/Values
    for k, v in params.items():
        log_j[k] = v

    if return_string:
        return log_j
    else:
        print(JsonPlus().dumps(log_j))
