from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.calcul.observation.processJsonDataSum import ProcessJsonDataSum
import json
import datetime


class ProcessJsonDataSumOmm(ProcessJsonDataSum):
    """
        ProcessJsonDataAvgOmm

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
        if stop_dat.minute == 00 and stop_dat.second <= 2:
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
        """ generate deltaValues from ObsMeteor.data """
        if obs_meteor.data.stop_dat.minute == 00 and obs_meteor.data.stop_dat.second <= 2:
            super().loadDataInObs(
                my_measure,
                obs_meteor,
                target_key,
                delta_values,
                my_values,
                trace_flag,
            )

    def loadMaxMinInObs(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        target_key: str,
        delta_values: json,
        my_values: json,
        trace_flag: bool = False,
    ):
        if obs_meteor.data.stop_dat.minute == 00 and obs_meteor.data.stop_dat.second <= 2:
            super().loadMaxMinInObs(my_measure, obs_meteor, target_key, delta_values, my_values, trace_flag)
