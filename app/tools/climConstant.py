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

