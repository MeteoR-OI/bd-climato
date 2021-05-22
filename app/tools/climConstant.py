from app.tools.constantClass import Constants


class ClimConstants(Constants):
    """ general purpose constants """
    JSON_CURRENT = 'current'
    JSON_AGGREGATE = 'aggregate'


class MeasureProcessingBitMask(Constants):
    """ special measure processing"""
    Standard = 0
    MeasureIsWind = 1
    OnlyAggregateInHour = 2
    NotAllowedInCurrent = 4
    MeasureIsOmm = 128


class SvcRequestType(Constants):
    Nope = 0
    Start = 1
    Stop = 2
    Status = 4
    List = 8
    Run = 16
    TraceOn = 32
    TraceOff = 64


class ComputationParam(Constants):
    # parameter for calculus module
    AddHourToMeasureInAggHour = 1
