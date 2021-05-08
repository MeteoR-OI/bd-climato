from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.calcul.observation.processJsonData import ProcessJsonData
import json
import datetime


class ProcessJsonDataNo(ProcessJsonData):
    """
        ProcessJsonDataAvg

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """
    def loadValuesFromCurrent(
        self,
        my_measure: json,
        json_file_data: json,
        measure_idx: int,
        src_key: str,
        target_key: str,
        exclusion: json,
        my_values: json,
        stop_dat: datetime,
        trace_flag: bool,
    ):
        self._loadValuesFromCurrent(my_measure, json_file_data, measure_idx, src_key, target_key, exclusion, my_values, '_avg', stop_dat, trace_flag)

    def loadDataInObs(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        target_key: str,
        delta_values: json,
        my_values: json,
        trace_flag: bool,
    ):
        return
