from enum import Enum


class H_974:
    class RowId(Enum):
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

    pattern = [
        r'H_974_\d{4}-\d{4}\.csv',
        r'H_974_previous-\d{4}-\d{4}\.csv',
        r'H_974_latest-\d{4}-\d{4}\.csv'
    ]
    duration = 60
    poste_strategy = 1
    mappings = [
        {'csv_field': 'DD',        'csv_idx': RowId.DD.value, 'qa_idx': RowId.QDD.value,         'mesure': 'wind 10 dir',         'minmax': {}},
        {'csv_field': 'FF',        'csv_idx': RowId.FF.value, 'qa_idx': RowId.QFF.value,         'mesure': 'wind 10',          'minmax':
            {"max": RowId.FXY.value, "qmax": RowId.QFXY.value, "maxDir": RowId.DXY.value, "maxTime": RowId.HXY.value}},
        {'csv_field': 'FXI',       'csv_idx': RowId.FXI.value, 'qa_idx': RowId.QFXI.value,       'mesure': 'gust',             'minmax':
            {"max": RowId.FXI.value, "qmax": RowId.QFXI.value, "maxDir": RowId.DXI.value, "maxTime": RowId.HXI.value}},
        {'csv_field': 'DD2',       'csv_idx': RowId.DD2.value, 'qa_idx': RowId.QDD2.value,       'mesure': 'wind dir',         'minmax': {}},
        {'csv_field': 'FF2',       'csv_idx': RowId.FF2.value, 'qa_idx': RowId.QFF2.value,       'mesure': 'wind',             'minmax':
            {"max": RowId.FXI2.value, "qmax": RowId.QFXI2.value, "maxDir": RowId.DXI2.value, "maxTime": RowId.HXI2.value}},
        {'csv_field': 'GLO',       'csv_idx': RowId.GLO.value, 'qa_idx': RowId.QGLO.value,       'mesure': 'radiation',        'minmax': {}},
        {'csv_field': 'PMER',      'csv_idx': RowId.PMER.value, 'qa_idx': RowId.QPMER.value,     'mesure': 'barometer',        'minmax':
            {"min": RowId.PMERMIN.value, "qmin": RowId.QPERMIN.value}},
        {'csv_field': 'PSTAT',     'csv_idx': RowId.PSTAT.value, 'qa_idx': RowId.QPSTAT.value,   'mesure': 'pressure',         'minmax': {}},
        {'csv_field': 'RR1',       'csv_idx': RowId.RR1.value, 'qa_idx': RowId.QRR1.value,       'mesure': 'rain',             'minmax': {}},
        {'csv_field': 'T',         'csv_idx': RowId.T.value, 'qa_idx': RowId.QT.value,           'mesure': 'temperature',      'minmax':
            {"min": RowId.TN.value, "qmin": RowId.QTN.value, "minTime": RowId.HTN.value, "max": RowId.TX.value, "qmax": RowId.QTX.value, "maxTine": RowId.HTX.value}},
        {'csv_field': 'Temp Sol 10m', 'csv_idx': RowId.T10.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp1',      'minmax': {}},
        {'csv_field': 'Temp Sol 20m', 'csv_idx': RowId.T20.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp2',      'minmax': {}},
        {'csv_field': 'Temp Sol 50m', 'csv_idx': RowId.T50.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp3',      'minmax': {}},
        {'csv_field': 'Temp Sol 100m', 'csv_idx': RowId.T100.value, 'qa_idx': RowId.QT10.value,  'mesure': 'soiltemp4',      'minmax': {}},
        {'csv_field': 'TD',        'csv_idx': RowId.TD.value, 'qa_idx': RowId.QTD.value,         'mesure': 'dewpoint',         'minmax': {}},
        {'csv_field': 'TVEGETAUX', 'csv_idx': RowId.TVEGETAUX.value, 'qa_idx': RowId.QTVEGETAUX.value,    'mesure': 'leaftemp1',        'minmax': {}},
        {'csv_field': 'U',         'csv_idx': RowId.U.value, 'qa_idx': RowId.QU.value,           'mesure': 'humidity',         'minmax':
            {"min": RowId.UN.value, "qmin": RowId.QUN.value, "minTime": RowId.HUN.value, "max": RowId.UX.value, "qmax": RowId.QUX.value, "maxTine": RowId.HUX.value}},
        {'csv_field': 'UV',        'csv_idx': RowId.UV_INDICE.value, 'qa_idx': RowId.QUV_INDICE.value,         'mesure': 'uv_indice',        'minmax': {}},
        {'csv_field': 'GLO',       'csv_idx': RowId.GLO.value,     'qa_idx': RowId.QGLO.value,   'mesure': 'radiation',        'minmax': {}},
    ]

# NUM_POSTE   : numéro Météo-France du poste sur 8 chiffres
# NOM_USUEL   : nom usuel du poste
# LAT         : latitude, négative au sud (en degrés et millionièmes de degré)
# LON         : longitude, négative à l’ouest de GREENWICH (en degrés et millionièmes de degré)
# ALTI        : altitude du pied de l'abri ou du pluviomètre si pas d'abri (en m)
# AAAAMMJJHH  : date de la mesure (année mois jour heure)
    
# RR1         : quantité de précipitation tombée en 1 heure (en mm et 1/10 mm)
DRR1        : durée des précipitations (en mn)
# FF          : force du vent moyenné sur 10 mn, mesurée à 10 m (en m/s et 1/10)
# DD          : direction de FF (en rose de 360)
# FXY         : valeur maximale de FF dans l’heure (en m/s et 1/10)
# DXY         : direction de FXY (rose de 360)
# HXY         : heure de FXY (hhmm)
# FXI         : force maximale du vent instantané dans l’heure, mesurée à 10 m (en m/s et 1/10)
# DXI         : direction de FXI (en rose de 360)
# HXI         : heure de FXI (hhmm)
# FF2         : force du vent moyenné sur 10 mn, mesurée à 2 m (en m/s et 1/10)
# DD2         : direction de FF2 (en rose de 360)
# FXI2        : force maximale du vent instantané dans l’heure, mesurée à 2 m (en m/s et 1/10)
# DXI2        : direction de FXI2 (en rose de 360)
# HXI2        : heure de FXI2 (hhmm)
FXI3S       : force maximale du vent moyenné sur 3 secondes dans l’heure (en m/s et 1/10)
DXI3S       : direction de FXI3S (en rose de 360)
HXI3S       : heure de FXI3S (hhmm)
# T           : température sous abri instantanée (en °C et 1/10)
# TD          : température du point de rosée (en °C et 1/10)
# TN          : température minimale sous abri dans l’heure (en °C et 1/10)
# HTN         : heure de TN (hhmm)
# TX          : température maximale sous abri dans l’heure (en °C et 1/10)
# HTX         : heure de TX (hhmm)
DG          : durée de gel sous abri (T ≤ 0°C) (en mn)
# T10         : température à 10 cm au-dessous du sol (en °C et 1/10), n’existe pas pour les sémaphores
# T20         : température à 20 cm au-dessous du sol (en °C et 1/10), n’existe pas pour les sémaphores
# T50         : température à 50 cm au-dessous du sol (en °C et 1/10), n’existe pas pour les sémaphores
# T100        : température à 1 m au-dessous du sol (en °C et 1/10), n’existe pas pour les sémaphores
TNSOL       : température minimale à 10 cm au-dessus du sol (en °C et 1/10)
TN50        : température minimale à 50 cm au-dessus du sol (en °C et 1/10)
TCHAUSSEE   : température de surface mesurée sur herbe ou sur bitume (en °C et 1/10)
DHUMEC      : durée d’humectation (en mn)
# U           : humidité relative (en %)
# UN          : humidité relative minimale dans l’heure (en %)
# HUN         : heure de UN (hhmm)
# UX          : humidité relative maximale dans l’heure (en %)
# HUX         : heure de UX (hhmm)
DHUMI40     : durée avec humidité ≤ 40% (en mn)
DHUMI80     : durée avec humidité ≥ 80% (en mn)
TSV         : tension de vapeur (en hPa et 1/10)
# PMER        : pression mer, seulement pour les postes dont l’altitude est inférieure ou égale à 750 m (en hPa et 1/10)
# PSTAT       : pression station (en hPa et 1/10)
# PMERMIN     : minimum horaire de la pression mer (en hPa et 1/10)
GEOP        : géopotentiel, seulement pour les stations dont l’altitude est supérieure à 750 m (en mgp)
N           : nébulosité totale (en octa), 9=ciel invisible par brouillard et/ou autre phénomène météorologique
NBAS        : nébulosité de la couche nuageuse principale la plus basse (en octa)
CL          : code SYNOP nuages bas (v. Atlas international des nuages (OMM-N°407), Volume I, Classification des nuages)
CM          : code SYNOP nuages moyens (v. Atlas international des nuages (OMM-N°407), Volume I, Classification des nuages)
CH          : code SYNOP nuages élevés (v. Atlas international des nuages (OMM-N°407), Volume I, Classification des nuages)
N1          : nébulosité de la 1ère couche nuageuse (en octa)
C1          : genre de la 1ère couche nuageuse
B1          : base de la 1ère couche nuageuse (en m)
N2          : nébulosité de la 2ème couche nuageuse (en octa)
C2          : genre de la 2ème couche nuageuse
B2          : base de la 2ème couche nuageuse (en m)
N3          : nébulosité de la 3ème couche nuageuse (en octa)
C3          : genre de la 3ème couche nuageuse
B3          : base de la 3ème couche nuageuse (en m)
N4          : nébulosité de la 4ème couche nuageuse (en octa)
C4          : genre de la 4ème couche nuageuse
B4          : base de la 4ème couche nuageuse (en m)
VV          : visibilité (en m)
DVV200      : durée avec visibilité < 200 m (en mn)
WW          : code descriptif du temps présent (WMO Manuel des codes, Volume I.1, Section C-b, table 4677)
W1          : code descriptif du temps passé 1 (WMO Manuel des codes, Volume I.1, Section C-b, table 4687)
W2          : code descriptif du temps passé 2 (WMO Manuel des codes, Volume I.1, Section C-b, table 4687)
SOL         : état du sol sans neige : 
0 | surface du sol sèche (sans fissure et sans poussière ni sable meuble en quantité appréciable)
1 | surface du sol humide
2 | surface du sol mouillée (eau stagnante en mares, petites ou grandes, à la surface)
3 | inondé
4 | surface du sol gelée
5 | verglas au sol
6 | poussière ou sable meuble sec ne couvrant pas complètement le sol
7 | couche fine de poussière ou de sable meuble couvrant complètement le sol
8 | couche épaisse ou d'épaisseur moyenne de poussière ou de sable meuble couvrant complètement le sol
9 | très sec avec fissures
SOLNG       : état du sol avec neige : 
0 | sol en grande partie couvert de glace
1 | neige compacte ou mouillée (avec ou sans glace) couvrant moins de la moitié du sol
2 | neige compacte ou mouillée (avec ou sans glace) couvrant au moins la moitié du sol, mais ne le couvrant pas complètement
3 | couche uniforme de neige compacte ou mouillée couvrant complètement le sol
4 | couche non uniforme de neige compacte ou mouillée couvrant complètement le sol
5 | neige sèche poudreuse couvrant moins de la moitié du sol
6 | neige sèche poudreuse couvrant au moins la moitié du sol, mais ne le couvrant pas complètement
7 | couche uniforme de neige sèche poudreuse couvrant complètement le sol
8 | couche non uniforme de neige sèche poudreuse couvrant complètement le sol
9 | neige couvrant complètement le sol
TMER        : température de la mer (en °C et 1/10)
VVMER       : visibilité vers la mer, codée de 0 à 9 :
0 | moins de 50 m
1 | 50 à 200 m exclu
2 | 200 à 500 m exclu
3 | 500 à 1000 m exclu
4 | 1 à 2 km exclu
5 | 2 à 4 km exclu
6 | 4 à 10 km exclu
7 | 10 à 20 km exclu
8 | 20 à 50 km exclu
9 | 50 km ou plus
ETATMER     : état de la mer pour les sémaphores :		
0 | calme (sans ride)
1 | calme (ridée)
2 | belle (vaguelettes)
3 | peu agitée
4 | agitée
5 | forte
6 | très forte
7 | grosse
8 | très grosse
9 | énorme
DIRHOULE    : direction de la houle pour les sémaphores et égale à 999 si la direction est variable (rose de 360)
HVAGUE      : hauteur des vagues, en particulier les bouées fixes (en m et 1/10)
PVAGUE      : période des vagues (en s et 1/10)
HNEIGEF     : hauteur de neige fraîche tombée en 6h, toujours renseignée aux heures synoptiques principales (en cm)
NEIGETOT    : hauteur de neige totale au sol (en cm)
TSNEIGE     : température de surface de la neige (en °C et 1/10)
TUBENEIGE   : enfoncement du tube de neige (en cm)
HNEIGEFI3   : hauteur de neige fraîche tombée en 3h, facultatif aux heures synoptiques intermédiaires (en cm)
HNEIGEFI1   : hauteur de neige fraîche tombée en 1h, facultatif aux heures non synoptiques (en cm)
ESNEIGE     : code descriptif de l’état de la neige pour les postes nivométéorologiques :
0 | neige fraîche (ou récente) sèche
1 | givre de surface
2 | neige fraîche (ou récente) humide
3 | neige soufflée non portante
4 | neige soufflée portante
5 | vieille neige humide portante ou non portante
6 | vieille neige sèche et meuble (non croûtée, non soufflée)
7 | croûte de regel non portante
8 | croûte de regel portante
9 | surface lisse et glacée
CHARGENEIGE : charge de la neige (en kg/m2)
# GLO         : rayonnement global horaire en heure UTC (en J/cm2)
GLO2        : rayonnement global horaire en heure TSV (en J/cm2)
DIR         : rayonnement direct horaire en heure UTC (en J/cm2)
DIR2        : rayonnement direct horaire en heure TSV (en J/cm2)
DIF         : rayonnement diffus horaire en heure UTC (en J/cm2)
DIF2        : rayonnement diffus horaire en heure TSV (en J/cm2)
# UV          : rayonnement ultra-violet horaire en heure UTC (en J/cm2)
UV2         : rayonnement ultra-violet horaire en heure TSV (en J/cm2)
# UV_INDICE   : indice UV (compris entre 0 et 12)
INFRAR      : rayonnement infra-rouge horaire en heure UTC (en J/cm2)
INFRAR2     : rayonnement infra-rouge horaire en heure TSV (en J/cm2)
INS         : insolation horaire en heure UTC (en mn)
INS2        : insolation horaire en heure TSV (en mn)
TLAGON      : température du lagon (en °C et 1/10)
# TVEGETAUX   : température des végétaux (en °C et 1/10)
ECOULEMENT  : niveau d’écoulement
