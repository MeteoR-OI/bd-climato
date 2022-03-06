from app.models import Observation, AggHour, AggDay, AggMonth, AggYear, AggAll, AggTodo, ExtremeTodo, AggHisto, Incident


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
    else:
        raise Exception("getAggTableName", "wrong niveau_agg: " + niveau_agg)


def doesObservationExist(obs_id: int, is_tmp: bool) -> bool:
    return Observation.objects.filter(id=obs_id).exists()


def doesAggExist(agg_id: int, agg_level: str) -> bool:
    agg_table = getAggTable(agg_level)
    return agg_table.objects.filter(id=agg_id).exists()


def delete_obs_agg(is_tmp: bool = None):
    """clean_up all our tables"""

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
