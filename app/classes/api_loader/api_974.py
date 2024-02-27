from app.classes.csv_loader.csvFileDef import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from enum import Enum


class RowsId(Enum):
    NUM_POSTE = 0
    NOM_USUEL = 1
    LAT = 2
    LON = 3
    ALTI = 4
    AAAAMMJJHH = 5
    RR1 = 6
    QRR1 = 7
    DRR1 = 8
    QDRR1 = 9
    FF = 10
    QFF = 11
    DD = 12
    QDD = 13
    FXY = 14
    QFXY = 15
    DXY = 16
    QDXY = 17
    HXY = 18
    QHXY = 19
    FXI = 20
    QFXI = 21
    DXI = 22
    QDXI = 23
    HXI = 24
    QHXI = 25
    FF2 = 26
    QFF2 = 27
    DD2 = 28
    QDD2 = 29
    FXI2 = 30
    QFXI2 = 31
    DXI2 = 32
    QDXI2 = 33
    HXI2 = 34
    QHXI2 = 35
    FXI3S = 36
    QFXI3S = 37
    DXI3S = 38
    QDXI3S = 39
    HFXI3S = 40
    QHFXI3S = 41
    T = 42
    QT = 43
    TD = 44
    QTD = 45
    TN = 46
    QTN = 47
    HTN = 48
    QHTN = 49
    TX = 50
    QTX = 51
    HTX = 52
    QHTX = 53
    DG = 54
    QDG = 55
    T10 = 56
    QT10 = 57
    T20 = 58
    QT20 = 59
    T50 = 60
    QT50 = 61
    T100 = 62
    QT100 = 63
    TNSOL = 64
    QTNSOL = 65
    TN50 = 66
    QTN50 = 67
    TCHAUSSEE = 68
    QTCHAUSSEE = 69
    DHUMEC = 70
    QDHUMEC = 71
    U = 72
    QU = 73
    UN = 74
    QUN = 75
    HUN = 76
    QHUN = 77
    UX = 78
    QUX = 79
    HUX = 80
    QHUX = 81
    DHUMI40 = 82
    QDHUMI40 = 83
    DHUMI80 = 84
    QDHUMI80 = 85
    TSV = 86
    QTSV = 87
    PMER = 88
    QPMER = 89
    PSTAT = 90
    QPSTAT = 91
    PMERMIN = 92
    QPERMIN = 93
    GEOP = 94
    QGEOP = 95
    N = 96
    QN = 97
    NBAS = 98
    QNBAS = 99
    CL = 100
    QCL = 101
    CM = 102
    QCM = 103
    CH = 104
    QCH = 105
    N1 = 106
    QN1 = 107
    C1 = 108
    QC1 = 109
    B1 = 110
    QB1 = 111
    N2 = 112
    QN2 = 113
    C2 = 114
    QC2 = 115
    B2 = 116
    QCB2 = 117
    N3 = 118
    QN3 = 119
    C3 = 120
    QC3 = 121
    B3 = 122
    QB3 = 123
    N4 = 124
    QN4 = 125
    C4 = 126
    QC4 = 127
    B4 = 128
    QB4 = 129
    VV = 130
    QVV = 131
    DVV200 = 132
    QDVV200 = 133
    WW = 134
    QWW = 135
    W1 = 136
    QW1 = 137
    W2 = 138
    QW2 = 139
    SOL = 140
    QSOL = 141
    SOLNG = 142
    QSOLNG = 143
    TMER = 144
    QTMER = 145
    VVMER = 146
    QVVMER = 147
    ETATMER = 148
    QETATMER = 149
    DIRHOULE = 150
    QDIRHOULE = 151
    HVAGUE = 152
    QHVAGUE = 153
    PVAGUE = 154
    QPVAGUE = 155
    HNEIGEF = 156
    QHNEIGEF = 157
    NEIGETOT = 158
    QNEIGETOT = 159
    TSNEIGE = 160
    QTSNEIGE = 161
    TUBENEIGE = 162
    QTUBENEIGE = 163
    HNEIGEFI3 = 164
    QHNEIGEFI3 = 165
    HNEIGEFI1 = 166
    QHNEIGEFI1 = 167
    ESNEIGE = 168
    QESNEIGE = 169
    CHARGENEIGE = 170
    QCHARGENEIGE = 171
    GLO = 172
    QGLO = 173
    GLO2 = 174
    QGLO2 = 175
    DIR = 176
    QDIR = 177
    DIR2 = 178
    QDIR2 = 179
    DIF = 180
    QDIF = 181
    DIF2 = 182
    QDIF2 = 183
    UV = 184
    QUV = 185
    UV2 = 186
    QUV2 = 187
    UV_INDICE = 188
    QUV_INDICE = 189
    INFRAR = 190
    QINFRAR = 191
    INFRAR2 = 192
    QINFRAR2 = 193
    INS = 194
    QINS = 195
    INS2 = 196
    QINS2 = 197
    TLAGON = 198
    QTLAGON = 199
    TVEGETAUX = 200
    QTVEGETAUX = 201
    ECOULEMENT = 202
    QECOULEMENT = 203


class Api974(CsvFileSpec):

    def __init__(self):
        super().__init__({
                'pattern': [
                    r'H_974_\d{4}-\d{4}\.csv',
                    r'H_974_previous-\d{4}-\d{4}\.csv',
                    r'H_974_latest-\d{4}-\d{4}\.csv'
                ],
                'mappings': [
                    {'csv_field': 'DD',        'csv_idx': RowsId.DD.value, 'qa_idx': RowsId.QDD.value,         'mesure': 'wind 10 dir',         'minmax': {}},
                    {'csv_field': 'FF',        'csv_idx': RowsId.FF.value, 'qa_idx': RowsId.QFF.value,         'mesure': 'wind 10',          'minmax':
                        {"max": RowsId.FXY.value, "qmax": RowsId.QFXY.value, "maxDir": RowsId.DXY.value, "maxTime": RowsId.HXY.value}},
                    {'csv_field': 'FXI',       'csv_idx': RowsId.FXI.value, 'qa_idx': RowsId.QFXI.value,       'mesure': 'gust',             'minmax':
                        {"max": RowsId.FXI.value, "qmax": RowsId.QFXI.value, "maxDir": RowsId.DXI.value, "maxTime": RowsId.HXI.value}},
                    {'csv_field': 'DD2',       'csv_idx': RowsId.DD2.value, 'qa_idx': RowsId.QDD2.value,       'mesure': 'wind dir',         'minmax': {}},
                    {'csv_field': 'FF2',       'csv_idx': RowsId.FF2.value, 'qa_idx': RowsId.QFF2.value,       'mesure': 'wind',             'minmax':
                        {"max": RowsId.FXI2.value, "qmax": RowsId.QFXI2.value, "maxDir": RowsId.DXI2.value, "maxTime": RowsId.HXI2.value}},
                    {'csv_field': 'GLO',       'csv_idx': RowsId.GLO.value, 'qa_idx': RowsId.QGLO.value,       'mesure': 'radiation',        'minmax': {}},
                    {'csv_field': 'PMER',      'csv_idx': RowsId.PMER.value, 'qa_idx': RowsId.QPMER.value,     'mesure': 'barometer',        'minmax':
                        {"min": RowsId.PMERMIN.value, "qmin": RowsId.QPERMIN.value}},
                    {'csv_field': 'PSTAT',     'csv_idx': RowsId.PSTAT.value, 'qa_idx': RowsId.QPSTAT.value,   'mesure': 'pressure',         'minmax': {}},
                    {'csv_field': 'RR1',       'csv_idx': RowsId.RR1.value, 'qa_idx': RowsId.QRR1.value,       'mesure': 'rain',             'minmax': {}},
                    {'csv_field': 'T',         'csv_idx': RowsId.T.value, 'qa_idx': RowsId.QT.value,           'mesure': 'temperature',      'minmax':
                        {"min": RowsId.TN.value, "qmin": RowsId.QTN.value, "minTime": RowsId.HTN.value, "max": RowsId.TX.value, "qmax": RowsId.QTX.value, "maxTine": RowsId.HTX.value}},
                    {'csv_field': 'Temp Sol 10m', 'csv_idx': RowsId.T10.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp1',      'minmax': {}},
                    {'csv_field': 'Temp Sol 20m', 'csv_idx': RowsId.T20.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp2',      'minmax': {}},
                    {'csv_field': 'Temp Sol 50m', 'csv_idx': RowsId.T50.value, 'qa_idx': RowsId.QT10.value,    'mesure': 'soiltemp3',      'minmax': {}},
                    {'csv_field': 'Temp Sol 100m', 'csv_idx': RowsId.T100.value, 'qa_idx': RowsId.QT10.value,  'mesure': 'soiltemp4',      'minmax': {}},
                    {'csv_field': 'TD',        'csv_idx': RowsId.TD.value, 'qa_idx': RowsId.QTD.value,         'mesure': 'dewpoint',         'minmax': {}},
                    {'csv_field': 'TVEGETAUX', 'csv_idx': RowsId.TVEGETAUX.value, 'qa_idx': RowsId.QTVEGETAUX.value,    'mesure': 'leaftemp1',        'minmax': {}},
                    {'csv_field': 'U',         'csv_idx': RowsId.U.value, 'qa_idx': RowsId.QU.value,           'mesure': 'humidity',         'minmax':
                        {"min": RowsId.UN.value, "qmin": RowsId.QUN.value, "minTime": RowsId.HUN.value, "max": RowsId.UX.value, "qmax": RowsId.QUX.value, "maxTine": RowsId.HUX.value}},
                    {'csv_field': 'UV',        'csv_idx': RowsId.UV_INDICE.value, 'qa_idx': RowsId.QUV_INDICE.value,         'mesure': 'uv_indice',        'minmax': {}},
                    {'csv_field': 'GLO',       'csv_idx': RowsId.GLO.value,     'qa_idx': RowsId.QGLO.value,   'mesure': 'radiation',        'minmax': {}},
                ],
                'skip_lines': 1,
                'poste_strategy': 1,
            })

    def getPosteData(self, rows):
        return {
                'meteor': rows[RowsId.NOM_USUEL.value],
                'ALTI': rows[RowsId.ALTI.value],
                'LAT': rows[RowsId.LAT.value],
                'LON': rows[RowsId.LON.value],
                'CODE': rows[RowsId.NUM_POSTE.value].strip()
        }

    def hackHeader(self, header):
        return header

    def getStopDate(self, rows):
        tmp_dt = rows[RowsId.AAAAMMJJHH.value]
        return str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':00:00')
