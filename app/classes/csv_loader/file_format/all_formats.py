from app.classes.csv_loader.file_format.H_974_files import H_974
from app.classes.csv_loader.file_format.Q_974_autres_param_files import Q_974_autres_param
from app.classes.csv_loader.file_format.Q_974_RR_T_Vent_files import Q_974_RR_T_Vent


all_formats = [
    H_974(),
    Q_974_autres_param(),
    Q_974_RR_T_Vent()
]
