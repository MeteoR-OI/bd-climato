from app.models import Observation, AggHour, AggDay, AggMonth, AggYear, AggAll, AggHisto, AggTodo
from app.models import TmpObservation, TmpAggHour, TmpAggDay, TmpAggMonth, TmpAggYear, TmpAggAll, TmpAggHisto, TmpAggTodo


def isTmpLevel(agg_level: str) -> bool:
    """get the aggregation depending on the level"""
    if agg_level in ["H", "D", "M", "Y", "A"]:
        return False
    if agg_level in ["HT", "DT", "MT", "YT", "AT"]:
        return True

    raise Exception("Invalid aggregation level: " + agg_level)


def getObservationTable(is_tmp: bool):
    if is_tmp is True:
        return TmpObservation
    return Observation


def getAggHistoTable(agg_level: str):
    if isTmpLevel(agg_level) is False:
        return AggHisto
    return TmpAggHisto


def getAggHistoTableWithBool(is_tmp: bool):
    if is_tmp is False:
        return AggHisto
    return TmpAggHisto


def getAggTable(niveau_agg: str):
    """get the aggregation depending on the level"""
    if niveau_agg == "H":
        return AggHour
    elif niveau_agg == "D":
        return AggDay
    elif niveau_agg == "M":
        return AggMonth
    elif niveau_agg == "Y":
        return AggYear
    elif niveau_agg == "A":
        return AggAll
    elif niveau_agg == "HT":
        return TmpAggHour
    elif niveau_agg == "DT":
        return TmpAggDay
    elif niveau_agg == "MT":
        return TmpAggMonth
    elif niveau_agg == "YT":
        return TmpAggYear
    elif niveau_agg == "AT":
        return TmpAggAll
    else:
        raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)


def getAggTableName(niveau_agg: str):
    """get the aggregation depending on the level"""
    if niveau_agg == "H":
        return "AggHour"
    elif niveau_agg == "D":
        return "AggDay"
    elif niveau_agg == "M":
        return "AggMonth"
    elif niveau_agg == "Y":
        return "AggYear"
    elif niveau_agg == "A":
        return "AggAll"
    elif niveau_agg == "HT":
        return "TmpAggHour"
    elif niveau_agg == "DT":
        return "TmpAggDay"
    elif niveau_agg == "MT":
        return "TmpAggMonth"
    elif niveau_agg == "YT":
        return "TmpAggYear"
    elif niveau_agg == "AT":
        return "TmpAggAll"
    else:
        raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)


def getAggTodoObject(is_tmp: bool):
    """get the aggregation depending on the level"""
    if is_tmp is False:
        return AggTodo
    return TmpAggTodo


def doesObservationExist(obs_id: int, is_tmp: bool) -> bool:
    obs_table = getObservationTable(is_tmp)
    return obs_table.objects.filter(id=obs_id).exists()


def doesAggExist(agg_id: int, agg_level: str) -> bool:
    agg_table = getAggTable(agg_level)
    return agg_table.objects.filter(id=agg_id).exists()
