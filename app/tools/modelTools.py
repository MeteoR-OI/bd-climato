from app.models import Observation, AggHour, AggDay, AggMonth, AggYear, AggAll, AggTodo, ExtremeTodo, AggHisto, Incident
from app.models import TmpObservation, TmpAggHour, TmpAggDay, TmpAggMonth, TmpAggYear, TmpAggAll, TmpAggTodo, TmpExtremeTodo, TmpAggHisto


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
        raise Exception("getAggTable", "wrong niveau_agg: " + niveau_agg)


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
        raise Exception("getAggTableName", "wrong niveau_agg: " + niveau_agg)


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


def delete_obs_agg(is_tmp: bool = None):
    """clean_up all our tables"""
    if is_tmp is None:
        raise Exception('AllCalculus::delete_obs_agg', 'is_tmp not given')

    if is_tmp is False:
        AggHisto.objects.all().delete()
        Observation.objects.all().delete()
        AggHour.objects.all().delete()
        AggDay.objects.all().delete()
        AggMonth.objects.all().delete()
        AggYear.objects.all().delete()
        AggAll.objects.all().delete()
        AggTodo.objects.all().delete()
        ExtremeTodo.objects.all().delete()
        Incident.objects.all().delete()
    else:
        TmpAggHisto.objects.all().delete()
        TmpObservation.objects.all().delete()
        TmpAggHour.objects.all().delete()
        TmpAggDay.objects.all().delete()
        TmpAggMonth.objects.all().delete()
        TmpAggYear.objects.all().delete()
        TmpAggAll.objects.all().delete()
        TmpAggTodo.objects.all().delete()
        TmpExtremeTodo.objects.all().delete()
