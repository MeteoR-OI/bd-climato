from enum import Enum


class RowsId(Enum):
    NUM_POSTE = 0
    NOM_USUEL = 1
    LAT = 2
    LON = 3
    ALTI = 4
    AAAAMMJJ = 5
    DHUMEC = 6
    QDHUMEC = 7
    PMERM = 8
    QPMERM = 9
    PMERMIN = 10
    QPMERMIN = 11
    INST = 12
    QINST = 13
    GLOT = 14
    QGLOT = 15
    DIFT = 16
    QDIFT = 17
    DIRT = 18
    QDIRT = 19
    INFRART = 20
    QINFRART = 21
    UV = 22
    QUV = 23
    UV_INDICEX = 24
    QUV_INDICEX = 25
    SIGMA = 26
    QSIGMA = 27
    UN = 28
    QUN = 29
    HUN = 30
    UX = 31
    QUX = 32
    HUX = 33
    QHUX = 34
    UM = 35
    QUM = 36
    DHUMI40 = 37
    QDHUMI40 = 38
    DHUMI80 = 39
    QDHUMI80 = 40
    TSVM = 41
    QTSVM = 42
    ETPMON = 43
    QETPMON = 44
    ETPGRILLE = 45
    QETPGRILLE = 46
    ECOULEMENTM = 47
    QECOULEMENTM = 48
    HNEIGEF = 49
    QHNEIGEF = 50
    NEIGETOTX = 51
    QNEIGETOTX = 52
    NEIGETOT06 = 53
    QNEIGETOT06 = 54
    NEIG = 55
    QNEIG = 56
    BROU = 57
    QBROU = 58
    ORAG = 59
    QORAG = 60
    GRESIL = 61
    QGRESIL = 62
    GRELE = 63
    QGRELE = 64
    ROSEE = 65
    QROSEE = 66
    VERGLAS = 67
    QVERGLAS = 68
    SOLNEIGE = 69
    QSOLNEIGE = 70
    GELEE = 71
    QGELEE = 72
    FUMEE = 73
    QFUMEE = 74
    BRUME = 75
    QBRUME = 76
    ECLAIR = 77
    QECLAIR = 78
    NB300 = 79
    QNB300 = 80
    BA300 = 81
    QBA300 = 82
    TMERMIN = 83
    QTMERMIN = 84
    TMERMAX = 85
    QTMERMAX = 86


mappings = [
    # {'csv_field': 'DD',        'csv_idx': RowsId.DD.value, 'qa_idx': RowsId.QDD.value,         'mesure': 'wind 10 dir',         'minmax': {}},
    {'csv_field': 'FFM',        'csv_idx': RowsId.FF.value, 'qa_idx': RowsId.QFF.value,         'mesure': 'wind 10',          'minmax':
        {"max": RowsId.FXY.value, "qmax": RowsId.QFXY.value, "maxDir": RowsId.DXY.value, "maxTime": RowsId.HXY.value}},
    {'csv_field': 'FXI',       'csv_idx': RowsId.FXI.value, 'qa_idx': RowsId.QFXI.value,       'mesure': 'gust',             'minmax':
        {"max": RowsId.FXI.value, "qmax": RowsId.QFXI.value, "maxDir": RowsId.DXI.value, "maxTime": RowsId.HXI.value}},
    # {'csv_field': 'DD2',       'csv_idx': RowsId.DD2.value, 'qa_idx': RowsId.QDD2.value,       'mesure': 'wind dir',         'minmax': {}},
    {'csv_field': 'FF2M',       'csv_idx': RowsId.FF2.value, 'qa_idx': RowsId.QFF2.value,       'mesure': 'wind',             'minmax':
        {"max": RowsId.FXI2.value, "qmax": RowsId.QFXI2.value, "maxDir": RowsId.DXI2.value, "maxTime": RowsId.HXI2.value}},
    # {'csv_field': 'GLO',       'csv_idx': RowsId.GLO.value, 'qa_idx': RowsId.QGLO.value,       'mesure': 'radiation',        'minmax': {}},
    {'csv_field': 'PMERM',      'csv_idx': RowsId.PMER.value, 'qa_idx': RowsId.QPMER.value,     'mesure': 'barometer',        'minmax':
        {"min": RowsId.PMERMIN.value, "qmin": RowsId.QPERMIN.value}},
    # {'csv_field': 'PSTAT',     'csv_idx': RowsId.PSTAT.value, 'qa_idx': RowsId.QPSTAT.value,   'mesure': 'pressure',         'minmax': {}},
    {'csv_field': 'RR',        'csv_idx': RowsId.RR1.value, 'qa_idx': RowsId.QRR1.value,       'mesure': 'rain',             'minmax': {}},
    {'csv_field': 'TM',         'csv_idx': RowsId.T.value, 'qa_idx': RowsId.QT.value,           'mesure': 'temperature',      'minmax':
        {"min": RowsId.TN.value, "qmin": RowsId.QTN.value, "minTime": RowsId.HTN.value, "max": RowsId.TX.value, "qmax": RowsId.QTX.value, "maxTine": RowsId.HTX.value}},
    {'csv_field': 'TNSOL', 'csv_idx': RowsId.T10.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp1',      'minmax': {}},
    # {'csv_field': 'Temp Sol 20m', 'csv_idx': RowsId.T20.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp2',      'minmax': {}},
    {'csv_field': 'TN50', 'csv_idx': RowsId.T50.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp3',      'minmax': {}},
    # {'csv_field': 'Temp Sol 100m', 'csv_idx': RowsId.T100.value, 'qa_idx': RowsId.QT10.value,  'mesure': 'soiltemp4',      'minmax': {}},
    # {'csv_field': 'TD',        'csv_idx': RowsId.TD.value, 'qa_idx': RowsId.QTD.value,         'mesure': 'dewpoint',         'minmax': {}},
    # {'csv_field': 'TVEGETAUX', 'csv_idx': RowsId.TVEGETAUX.value, 'qa_idx': RowsId.QTVEGETAUX.value,    'mesure': 'leaftemp1',        'minmax': {}},
    {'csv_field': 'U',         'csv_idx': RowsId.U.value, 'qa_idx': RowsId.QU.value,           'mesure': 'humidity',         'minmax':
        {"min": RowsId.UN.value, "qmin": RowsId.QUN.value, "minTime": RowsId.HUN.value, "max": RowsId.UX.value, "qmax": RowsId.QUX.value, "maxTine": RowsId.HUX.value}},
    {'csv_field': 'UV',        'csv_idx': RowsId.UV_INDICE.value, 'qa_idx': RowsId.QUV_INDICE.value,         'mesure': 'uv_indice',        'minmax': {}},
    {'csv_field': 'GLO',       'csv_idx': RowsId.GLO.value,     'qa_idx': RowsId.QGLO.value,   'mesure': 'radiation',        'minmax': {}},
]
