from app.tools.constantClass import Constants


class ClimConstants(Constants):
    """ general purpose constants """
    JSON_CURRENT = 'current'
    JSON_AGGREGATE = 'aggregate'


class MeasureProcessingBitMask(Constants):
    """ special measure processing"""
    Standard = 0
    MeasureIsSum = 1
    MeasureIsWind = 2
    OnlyAggregateInHour = 4
    NotAllowedInCurrent = 8
    MeasureIsOmm = 16


class SvcRequestType(Constants):
    Nope = 0
    Start = 1
    Stop = 2
    Status = 4
    List = 8
    Run = 16


class ComputationParam(Constants):
    # parameter for calculus module
    AddHourToMeasureInAggHour = 1


TelemetryConf = {
    "collector_endpoint": "localhost:14250",
    "insecure": True
}
