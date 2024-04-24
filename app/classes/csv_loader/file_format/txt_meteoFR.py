from enum import Enum
from app.models import Code_QA

class TxtMeteoFR:
    class RowId(Enum):
        POSTE = 0
        DATE = 1
        RR1 = 2
        QRR1 = 3
        T = 4
        QT = 5
        TD = 6
        QTD = 7
        TN = 8
        QTN = 9
        HTN = 10
        QHTN = 11
        TX = 12
        QTX = 13
        HTX = 14
        QHTX = 15
        PSTAT = 16
        QPSTAT = 17
        PMER = 18
        QPMER = 19
        PMERMIN = 20
        QPMERMIN = 21
        FF = 22
        QFF = 23
        DD = 24
        QDD = 25
        FXI = 26
        QFXI = 27
        DXI = 28
        QDXI = 29
        HXI = 30
        QHXI = 31
        U = 32
        QU = 33
        UN = 34
        QUN = 35
        HUN = 36
        QHUN = 37
        UX = 38
        QUX = 39
        HUX = 40
        QHUX = 41
        GLO = 42
        QGLO = 43

    pattern = [
        r'^.*.txt.data$',
    ]
    duration = 60
    poste_strategy = 1
    separator = ';'
    skip_lines = 1
    move_file = True
    mappings = [
        {'csv_field': 'RR1',       'csv_idx': RowId.RR1.value, 'qa_idx': RowId.QRR1.value,       'mesure': 'rain_utc',             'minmax': {}},
        {'csv_field': 'T',         'csv_idx': RowId.T.value, 'qa_idx': RowId.QT.value,           'mesure': 'temperature',      'minmax':
            {"min": RowId.TN.value, "qmin": RowId.QTN.value, "minTime": RowId.HTN.value, "max": RowId.TX.value, "qmax": RowId.QTX.value, "maxTine": RowId.HTX.value}},
        {'csv_field': 'TD',        'csv_idx': RowId.TD.value, 'qa_idx': RowId.QTD.value,         'mesure': 'dewpoint',       'minmax': {}},
        {'csv_field': 'PSTAT',     'csv_idx': RowId.PSTAT.value, 'qa_idx': RowId.QPSTAT.value,   'mesure': 'pressure',         'minmax': {}},
        {'csv_field': 'PMER',      'csv_idx': RowId.PMER.value, 'qa_idx': RowId.QPMER.value,     'mesure': 'barometer',        'minmax':
            {"min": RowId.PMERMIN.value, "qmin": RowId.QPMERMIN.value}},
        {'csv_field': 'FF',        'csv_idx': RowId.FF.value, 'qa_idx': RowId.QFF.value,         'mesure': 'wind',          'minmax':
            {"max": RowId.FXI.value, "qmax": RowId.QFXI.value, "maxDir": RowId.DXI.value, "maxTime": RowId.HXI.value}},
        {'csv_field': 'DD',       'csv_idx': RowId.DD.value, 'qa_idx': RowId.QDD.value,       'mesure': 'wind dir',         'minmax': {}},
        {'csv_field': 'U',         'csv_idx': RowId.U.value, 'qa_idx': RowId.QU.value,           'mesure': 'humidity',       'minmax':
            {"min": RowId.UN.value, "qmin": RowId.QUN.value, "minTime": RowId.HUN.value, "max": RowId.UX.value, "qmax": RowId.QUX.value, "maxTine": RowId.HUX.value}},
        {'csv_field': 'GLO',       'csv_idx': RowId.GLO.value, 'qa_idx': RowId.QGLO.value,       'mesure': 'radiation',        'minmax': {}},
    ]
    qa_mapping = [
        [['n'], Code_QA.UNSET.value],
        [['m'], Code_QA.UNSET.value],
        [['t'], Code_QA.VALIDATED.value],
        [['a'], Code_QA.VALIDATED.value],
        [['i'], Code_QA.VALIDATED.value],
        [['v'], Code_QA.VALIDATED.value],
        [['d'], Code_QA.UNVALIDATED.value],
        [['f'], Code_QA.UNVALIDATED.value],
    ]

# RR1	HAUTEUR DE PRECIPITATIONS HORAIRE	MILLIMETRES ET 1/10
# T	TEMPERATURE SOUS ABRI HORAIRE	DEG C ET 1/10
# TD	TEMPERATURE DU POINT DE ROSEE HORAIRE	DEG C ET 1/10
# TN	TEMPERATURE MINIMALE SOUS ABRI HORAIRE	DEG C ET 1/10
# HTN	HEURE DU TN SOUS ABRI HORAIRE	HEURES ET MINUTES
# TX	TEMPERATURE MAXIMALE SOUS ABRI HORAIRE	DEG C ET 1/10
# HTX	HEURE DU TX SOUS ABRI HORAIRE	HEURES ET MINUTES
# PSTAT	PRESSION STATION HORAIRE	HPA ET 1/10
# PMER	PRESSION MER HORAIRE	HPA ET 1/10
# PMERMIN	MINIMUM DE LA PRESSION MER	HPA ET 1/10
# FF	VITESSE DU VENT HORAIRE	M/S ET 1/10
# DD	DIRECTION DU VENT A 10 M HORAIRE	ROSE DE 360
# FXI	VITESSE DU VENT INSTANTANE MAXI HORAIRE	M/S ET 1/10
# DXI	DIRECTION DU VENT MAXI INSTANTANE HORAIRE	ROSE DE 360
# HXI	HEURE DU VENT MAX INSTANTANE HORAIRE	HEURES ET MINUTES
# U	HUMIDITE RELATIVE HORAIRE	%
# UN	HUMIDITE RELATIVE MINI HORAIRE	%
# HUN	HEURE DE L&apos;HUMIDITE RELATIVE MINIMALE HORAIRE	HEURES ET MINUTES
# UX	HUMIDITE RELATIVE MAXI HORAIRE	%
# HUX	HEURE DE L&apos;HUMIDITE RELATIVE MAXIMALE HORAIRE	HEURES ET MINUTES
# GLO	RAYONNEMENT GLOBAL HORAIRE	JOULES/CM2