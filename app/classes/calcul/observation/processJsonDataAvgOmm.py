from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.observation.processJsonDataAvg import ProcessJsonDataAvg
from app.tools.aggTools import delKey
import json


class ProcessJsonDataAvgOmm(ProcessJsonDataAvg):
    """
        ProcessJsonDataAvgOmm

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadData(
        self,
        my_measure: json,
        json_file_data: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        trace_flag: bool,
        isOmm: bool = False,
    ):
        # force the omm flag, which save the M_last_dat in the delta_values
        my_measure['special'] = my_measure['special'] | MeasureProcessingBitMask.MeasureIsOmm
        """ generate deltaValues from ObsMeteor.data """
        if obs_meteor.data.stop_dat.minute > 0 or obs_meteor.data.stop_dat.second > 1:
            return

        super(ProcessJsonDataAvgOmm, self).loadData(
            my_measure,
            json_file_data,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            trace_flag,
            True,
        )
        # we will invalidate only if our omm value is changed
        delKey(delta_values, target_key + '_maxmin_invalid_val_max')
        delKey(delta_values, target_key + '_maxmin_invalid_val_min')
