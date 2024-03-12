from enum import Enum


class Q_974_autres_param:
    class RowId(Enum):
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

    pattern = [
        r'H_974_\d{4}-\d{4}\_autres_parametres.csv',
        r'Q_974_previous-\d{4}-\d{4}\_autres_parametres.csv'
        r'Q_974_latest-\d{4}-\d{4}\_autres_parametres.csv'
    ]
    duration = 1440
    poste_strategy = 1
    mappings = [
        # {'csv_field': 'DD',        'csv_idx': RowId.DD.value, 'qa_idx': RowId.QDD.value,         'mesure': 'wind 10 dir',         'minmax': {}},
        {'csv_field': 'FFM',        'csv_idx': RowId.FF.value, 'qa_idx': RowId.QFF.value,         'mesure': 'wind 10',          'minmax':
            {"max": RowId.FXY.value, "qmax": RowId.QFXY.value, "maxDir": RowId.DXY.value, "maxTime": RowId.HXY.value}},
        {'csv_field': 'FXI',       'csv_idx': RowId.FXI.value, 'qa_idx': RowId.QFXI.value,       'mesure': 'gust',             'minmax':
            {"max": RowId.FXI.value, "qmax": RowId.QFXI.value, "maxDir": RowId.DXI.value, "maxTime": RowId.HXI.value}},
        # {'csv_field': 'DD2',       'csv_idx': RowId.DD2.value, 'qa_idx': RowId.QDD2.value,       'mesure': 'wind dir',         'minmax': {}},
        {'csv_field': 'FF2M',       'csv_idx': RowId.FF2.value, 'qa_idx': RowId.QFF2.value,       'mesure': 'wind',             'minmax':
            {"max": RowId.FXI2.value, "qmax": RowId.QFXI2.value, "maxDir": RowId.DXI2.value, "maxTime": RowId.HXI2.value}},
        # {'csv_field': 'GLO',       'csv_idx': RowId.GLO.value, 'qa_idx': RowId.QGLO.value,       'mesure': 'radiation',        'minmax': {}},
        {'csv_field': 'PMERM',      'csv_idx': RowId.PMER.value, 'qa_idx': RowId.QPMER.value,     'mesure': 'barometer',        'minmax':
            {"min": RowId.PMERMIN.value, "qmin": RowId.QPERMIN.value}},
        # {'csv_field': 'PSTAT',     'csv_idx': RowId.PSTAT.value, 'qa_idx': RowId.QPSTAT.value,   'mesure': 'pressure',         'minmax': {}},
        {'csv_field': 'RR',        'csv_idx': RowId.RR1.value, 'qa_idx': RowId.QRR1.value,       'mesure': 'rain',             'minmax': {}},
        {'csv_field': 'TM',         'csv_idx': RowId.T.value, 'qa_idx': RowId.QT.value,           'mesure': 'temperature',      'minmax':
            {"min": RowId.TN.value, "qmin": RowId.QTN.value, "minTime": RowId.HTN.value, "max": RowId.TX.value, "qmax": RowId.QTX.value, "maxTine": RowId.HTX.value}},
        {'csv_field': 'TNSOL', 'csv_idx': RowId.T10.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp1',      'minmax': {}},
        # {'csv_field': 'Temp Sol 20m', 'csv_idx': RowId.T20.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp2',      'minmax': {}},
        {'csv_field': 'TN50', 'csv_idx': RowId.T50.value, 'qa_idx': RowId.QT10.value,    'mesure': 'soiltemp3',      'minmax': {}},
        # {'csv_field': 'Temp Sol 100m', 'csv_idx': RowId.T100.value, 'qa_idx': RowId.QT10.value,  'mesure': 'soiltemp4',      'minmax': {}},
        # {'csv_field': 'TD',        'csv_idx': RowId.TD.value, 'qa_idx': RowId.QTD.value,         'mesure': 'dewpoint',         'minmax': {}},
        # {'csv_field': 'TVEGETAUX', 'csv_idx': RowId.TVEGETAUX.value, 'qa_idx': RowId.QTVEGETAUX.value,    'mesure': 'leaftemp1',        'minmax': {}},
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
# AAAAMMJJ    : date de la mesure (année mois jour)	
# DHUMEC      : durée d’humectation (en mn)	
# PMERM       : moyenne quotidienne des pressions mer horaires (en hPa et 1/10)	
# PMERMIN     : minimum quotidien des pressions mer minimales horaires (en hPa et 1/10)	
# INST        : durée d’insolation quotidienne (en mn)	
# GLOT        : rayonnement global quotidien (en J/cm2)	
# DIFT        : rayonnement diffus quotidien (en J/cm2)	
# DIRT        : rayonnement direct quotidien (en J/cm2)	
# INFRART     : somme des rayonnements infra-rouge horaires (en J/cm2)	
# UV          : cumul quotidien de rayonnement ultra-violet (en J/cm2)	
# UV_INDICEX  : maximum des indices UV horaires (en J/cm2)	
# SIGMA       : fraction d’insolation par rapport à la durée du jour (en %)	
# UN          : minimum quotidien des humidités relatives minimales horaires (en %)	
# HUN         : heure de UN (hhmm)	
# UX          : maximum quotidien des humidités relatives maximales horaires (en %)	
# HUX         : heure de UX (hhmm)	
# UM          : moyenne quotidienne des humidités relatives horaires (en %)	
# DHUMI40     : durée humidité avec U ≤ 40 % (en mn)	
# DHUMI80     : durée humidité U ≥ 80 % (en mn)	
# TSVM        : tension de vapeur moyenne (en hPa et 1/10)	
# ETPMON      : ETP Monteith quotidienne (en mm et 1/10)	
# ETPGRILLE   : ETP calculée au point de grille le plus proche (en mm et 1/10)	
# ECOULEMENTM : moyenne des niveaux d’écoulement horaires	
# HNEIGEF	    : hauteur de neige fraîche tombée en 24 heures (de 06h FU le jour J à 06h FU le jour J+1) qui reste au sol à 06h FU. La valeur relevée à J+1 est affectée au jour J (en cm)	
# NEIGETOTX   : épaisseur maximale de neige quotidienne (entre 01h et 24h FU) (en cm)	
# NEIGETOT06  : épaisseur totale de neige au sol mesurée à 6h (NEIGETOT de 6h) (en cm)	
# NEIG        : occurrence de neige (0 s’il n’a pas neigé, 1 s’il a neigé)	
# BROU        : occurrence de brouillard (0 ou 1 si phéno.)	
# ORAG        : occurrence d’orage (0 ou 1 si phéno.)	
# GRESIL      : occurrence de grésil (0 ou 1 si phéno.)	
# GRELE       : occurrence de grêle (0 ou 1 si phéno.)	
# ROSEE       : occurrence de rosée (0 ou 1 si phéno.)	
# VERGLAS     : occurrence de verglas (0 ou 1 si phéno.)	
# SOLNEIGE    : occurrence de sol couvert de neige (0 ou 1 si phéno.)	
# GELEE       : occurrence de gelée blanche (0 ou 1 si phéno.)	
# FUMEE       : occurrence de fumée (0 ou 1 si phéno.)	
# BRUME       : occurrence de brume (0 ou 1 si phéno.)	
# ECLAIR      : occurrence d’éclair (0 ou 1 si phéno)	
# NB300       : nébulosité maximale > 4/8 et couche < 300 m (en octa)	
# BA300       : hauteur minimale de NB300 (en m)	
# TMERMIN     : température minimale quotidienne de l’eau de mer (en °C et 1/10)	
# TMERMAX     : température maximale quotidienne de l’eau de mer (en °C et 1/10)	