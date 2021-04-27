from .jsonPlus import JsonPlus, json
import datetime
import inspect


def _logMe(message: str, level: str = None, span_id: str = None, params: json = {}, stack_level: int = 0, return_string: bool = False):
    """ centralized log output function """
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


def logException(inst, span_id: str = None, params: json = {}, return_string: bool = False):
    return _logMe(str(inst), 'error', span_id, params, 1, return_string)


def logInfo(message: str, span_id: str = None, params: json = {}, return_string: bool = False):
    return _logMe(message, 'info', span_id, params, 1, return_string)


def logTrace(message: str, span_id: str = None, params: json = {}, return_string: bool = False):
    return _logMe(message, 'trace', span_id, params, 1, return_string)

