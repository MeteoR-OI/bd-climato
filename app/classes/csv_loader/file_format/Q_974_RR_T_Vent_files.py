from enum import Enum


class Q_974_RR_T_Vent:
    class RowsId(Enum):
        NUM_POSTE = 0
        NOM_USUEL = 1
        LAT = 2
        LON = 3
        ALTI = 4
        AAAAMMJJ = 5
        RR = 6
        QRR = 7
        TN = 8
        QTN = 9
        HTN = 10
        QHTN = 11
        TX = 12
        QTX = 13
        HTX = 14
        QHTX = 15
        TM = 16
        QTM = 17
        TNTXM = 18
        QTNTXM = 19
        TAMPLI = 20
        QTAMPLI = 21
        TNSOL = 22
        QTNSOL = 23
        TN50 = 24
        QTN50 = 25
        DG = 26
        QDG = 27
        FFM = 28
        QFFM = 29
        FF2M = 30
        QFF2M = 31
        FXY = 32
        QFXY = 33
        DXY = 34
        QDXY = 35
        HXY = 36
        QHXY = 37
        FXI = 38
        QFXI = 39
        DXI = 40
        QDXI = 41
        HXI = 42
        QHXI = 43
        FXI2 = 44
        QFXI2 = 45
        DXI2 = 46
        QDXI2 = 47
        HXI2 = 48
        QHXI2 = 49
        FXI3S = 50
        QFXI3S = 51
        DXI3S = 52
        QDXI3S = 53
        HXI3S = 54
        QHXI3S = 55

    pattern = [
        r'H_974_\d{4}-\d{4}\_RR-T-Vent.csv',
        r'Q_974_previous-\d{4}-\d{4}\_RR-T-Vent.csv'
        r'Q_974_latest-\d{4}-\d{4}\_RR-T-Vent.csv'
    ]
    duration = 1440
    poste_strategy = 1
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

# NUM_POSTE   : numéro Météo-France du poste sur 8 chiffres
# NOM_USUEL   : nom usuel du poste
# LAT         : latitude, négative au sud (en degrés et millionièmes de degré)
# LON         : longitude, négative à l’ouest de GREENWICH (en degrés et millionièmes de degré)
# ALTI        : altitude du pied de l'abri ou du pluviomètre si pas d'abri (en m)
# AAAAMMJJ    : date de la mesure (année mois jour)
# RR          : quantité de précipitation tombée en 24 heures (de 06h FU le jour J à 06h FU le jour J+1). La valeur relevée à J+1 est affectée au jour J (en mm et 1/10)
# TN          : température minimale sous abri (en °C et 1/10)
# HTN         : heure de TN (hhmm)
# TX          : température maximale sous abri (en °C et 1/10)
# HTX         : heure de TX (hhmm)
# MT          : moyenne quotidienne des températures horaires sous abri (en °C et 1/10)
# no # TNTXM       : moyenne quotidienne (TN+TX)/2 (en °C et 1/10)
TAMPLI      : amplitude thermique quotidienne : écart entre TX et TN quotidiens (TX-TN) (en °C et 1/10)
# TNSOL       : température quotidienne minimale à 10 cm au-dessus du sol (en °C et 1/10)
# TN50        : température quotidienne minimale à 50 cm au-dessus du sol (en °C et 1/10)
DG          : durée de gel sous abri (T ≤ 0°C) (en mn)
FFM         : moyenne quotidienne de la force du vent moyenné sur 10 mn, à 10 m (en m/s et 1/10)
FF2M        : moyenne quotidienne de la force du vent moyenné sur 10 mn, à 2 m (en m/s et 1/10)
FXY         : maximum quotidien de la force maximale horaire du vent moyenné sur 10 mn, à 10 m (en m/s et 1/10)
DXY         : direction de FXY (en rose de 360)
HXY         : heure de FXY (hhmm)
FXI         : maximum quotidien de la force maximale horaire du vent instantané, à 10 m (en m/s et 1/10)
DXI         : direction de FXI (en rose de 360)
HXI         : heure de FXI (hhmm)
FXI2        : maximum quotidien de la force maximale horaire du vent instantané, à 2 m (en m/s et 1/10)
DXI2        : direction de FXI2 (en rose de 360)
HXI2        : heure de FXI2 (hhmm)
FXI3S       : maximum quotidien de la force maximale horaire du vent moyenné sur 3 s, à 10 m (en m/s et 1/10)
DXI3S       : direction de FXI3S (en rose de 360)
HXI3S       : heure de FXI3S (hhmm)