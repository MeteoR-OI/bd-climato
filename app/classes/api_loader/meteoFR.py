from enum import Enum

class API_Meteofr:

    class RowwId(Enum):
        NUM_POSTE = 1
        NOM_USUEL = 2
        LAT = 3
        LON = 4
        ALTI = 5
        AAAAMMJJHH = 6
        RR1 = 7
        QRR1 = 8
        DRR1 = 9
        QDRR1 = 10
        FF = 11
        QFF = 12
        DD = 13
        QDD = 14
        FXY = 15
        QFXY = 16
        DXY = 17
        QDXY = 18
        HXY = 19
        QHXY = 20
        FXI = 21
        QFXI = 22
        DXI = 23
        QDXI = 24
        HXI = 25
        QHXI = 26
        FF2 = 27
        QFF2 = 28
        DD2 = 29
        QDD2 = 30
        FXI2 = 31
        QFXI2 = 32
        DXI2 = 33
        QDXI2 = 34
        HXI2 = 35
        QHXI2 = 36
        FXI3S = 37
        QFXI3S = 38
        DXI3S = 39
        QDXI3S = 40
        HFXI3S = 41
        QHFXI3S = 42
        T = 43
        QT = 44
        TD = 45
        QTD = 46
        TN = 47
        QTN = 48
        HTN = 49
        QHTN = 50
        TX = 51
        QTX = 52
        HTX = 53
        QHTX = 54
        DureeGelSousAbri = 55
        QDG = 56
        T10 = 57
        QT10 = 58
        T20 = 59
        QT20 = 60
        T50 = 61
        QT50 = 62
        T100 = 63
        QT100 = 64
        TNSOL = 65
        QTNSOL = 66
        TN50 = 67
        QTN50 = 68
        TCHAUSSEE = 69
        QTCHAUSSEE = 70
        DHUMEC = 71
        QDHUMEC = 72
        U = 73
        QU = 74
        UN = 75
        QUN = 76
        HUN = 77
        QHUN = 78
        UX = 79
        QUX = 80
        HUX = 81
        QHUX = 82
        Duree_Humi_40% = 83
        QDHUMI40 = 84
        Duree_Humi_80% = 85
        QDHUMI80 = 86
        Tension_Vapeur = 87
        QTSV = 88
        PMER = 89
        QPMER = 90
        PSTAT = 91
        QPSTAT = 92
        PMERMIN = 93
        QPERMIN = 94
        g_potentiel = 95
        QGEOP = 96
        Nebulosite = 97
        QN = 98
        NBAS = 99
        QNBAS = 100
        CL = 101
        QCL = 102
        CM = 103
        QCM = 104
        CH = 105
        QCH = 106
        N1 = 107
        QN1 = 108
        C1 = 109
        QC1 = 110
        B1 = 111
        QB1 = 112
        N2 = 113
        QN2 = 114
        C2 = 115
        QC2 = 116
        B2 = 117
        QCB2 = 118
        N3 = 119
        QN3 = 120
        C3 = 121
        QC3 = 122
        B3 = 123
        QB3 = 124
        N4 = 125
        QN4 = 126
        C4 = 127
        QC4 = 128
        B4 = 129
        QB4 = 130
        VV = 131
        QVV = 132
        DVV200 = 133
        QDVV200 = 134
        WW = 135
        QWW = 136
        W1 = 137
        QW1 = 138
        W2 = 139
        QW2 = 140
        SOL = 141
        QSOL = 142
        SOLNG = 143
        QSOLNG = 144
        TMER = 145
        QTMER = 146
        VVMER = 147
        QVVMER = 148
        ETATMER = 149
        QETATMER = 150
        DIRHOULE = 151
        QDIRHOULE = 152
        HVAGUE = 153
        QHVAGUE = 154
        PVAGUE = 155
        QPVAGUE = 156
        HNEIGEF = 157
        QHNEIGEF = 158
        NEIGETOT = 159
        QNEIGETOT = 160
        TSNEIGE = 161
        QTSNEIGE = 162
        TUBENEIGE = 163
        QTUBENEIGE = 164
        HNEIGEFI3 = 165
        QHNEIGEFI3 = 166
        HNEIGEFI1 = 167
        QHNEIGEFI1 = 168
        ESNEIGE = 169
        QESNEIGE = 170
        CHARGENEIGE = 171
        QCHARGENEIGE = 172
        Rayonnement = 173
        QGLO = 174
        GLO2 = 175
        QGLO2 = 176
        DIR = 177
        QDIR = 178
        DIR2 = 179
        QDIR2 = 180
        DIF = 181
        QDIF = 182
        DIF2 = 183
        QDIF2 = 184
        UV = 185
        QUV = 186
        UV2 = 187
        QUV2 = 188
        UV_INDICE = 189
        QUV_INDICE = 190
        INFRAR = 191
        QINFRAR = 192
        INFRAR2 = 193
        QINFRAR2 = 194
        INS = 195
        QINS = 196
        INS2 = 197
        QINS2 = 198
        TLAGON = 199
        QTLAGON = 200
        TVEGETAUX = 201
        QTVEGETAUX = 202
        ECOULEMENT = 203
        QECOULEMENT = 204

    mappings = [
        # {'csv_field': 'DD',        'csv_idx': RowId.DD.value, 'qa_idx': RowId.QDD.value,         'mesure': 'wind 10 dir',         'minmax': {}},
    ]

# geo_id_insee ID of the point as defined by the INSEE number TEXT
# ddnnnpp (dd = department number, nnn = number of the municipality (ddnnn = Insee code),
# pp = accuracy on site)
# lat latitude in degrees REAL deg (plane angle)
# lon longitude in degrees REAL deg (plane angle)
# reference_time date and time of the production of the data in UTC TEXT iso8601/utc
# insert_time date and time of data-base insertion of the data in UTC TEXT iso8601/utc
# validity_time date and time of validity of the data in UTC TEXT iso8601/utc

# t air temperature at 2 meters above the ground in Kelvin degrees REAL K
# td air temperature of dew point at 2 meters above the ground in Kelvin degrees REAL K
# tx hourly maximum of air temperature at 2 meters above the ground in Kelvin degrees REAL K
# tn hourly minimum of air temperature at 2 meters above the ground in Kelvin degrees REAL K
# u hourly relative humidity at 2 meters INTEGER percent
# ux hourly maximum relative humidity at 2 meters INTEGER percent
# un hourly minimum relative humidity at 2 meters INTEGER percent
# dd mean wind direction at 10 meters above the ground in degrees INTEGER deg (direction)
# ff mean wind speed at 10 meters above the ground in m/s REAL m/s
# dxy hourly mean wind gust direction at 10 meters above the ground in degrees INTEGER deg (direction)
# fxy hourly mean wind gust speed at 10 meters above the ground over the previous 1H in m/s REAL m/s
# dxi hourly instant wind gust direction at 10 meters above the ground in degrees INTEGER deg (direction)
# fxi hourly instant wind gust speed at 10 meters above the ground over the previous 1H in m/s REAL m/s
# rr1 all precipitation over the previous 1H in mm REAL mm
# t_10 temperature at 10 centimeters below the ground in Kelvin degrees REAL K
# t_20 temperature at 20 centimeters below the ground in Kelvin degrees REAL K
# t_50 temperature at 50 centimeters below the ground in Kelvin degrees REAL K
# t_100 temperature at 1 meter below the ground in Kelvin degrees REAL K
vv horizontal visibility in meters INTEGER m
etat_sol ground state code INTEGER
sss total depth of snow cover in meters REAL m
n total nebulosity in octas INTEGER percent
insolh sunshine duration over the previous 1H REAL mn
# ray_glo01 hourly global radiation in J/m2 REAL J/m²
# pres station pressure in Pa REAL Pa
# pmer sea level pressure in Pa REAL 

