from app.tools.constantClass import Constants


class ClimConstants(Constants):
    """ general purpose constants """
    JSON_CURRENT = 'current'
    JSON_AGGREGATE = 'aggregate'


class AggLevelConstant(Constants):
    """ code agregation """
    Hour = 'H'
    Day = 'D'
    Month = 'M'
    Year = 'Y'
    All = 'A'


AggLevel = ['H', 'D', 'M', 'Y', 'A']


class MeasureProcessingBitMask(Constants):
    """ special measure processing"""
    Standard = 0
    MeasureIsSum = 1
    MeasureIsWind = 2
    OnlyAggregateInHour = 4
    NoAvgField = 8
    IsOmmMeasure = 16
    DoNotProcessTwiceInObs = 32     # when a measure is used multiple time in rootTypeInstr.mapping
