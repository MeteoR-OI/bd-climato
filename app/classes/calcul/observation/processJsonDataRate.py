from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.calcul.observation.processJsonDataAvg import ProcessJsonDataAvg
import json


class ProcessJsonDataRate(ProcessJsonDataAvg):
    """
        ProcessJsonDataRate

        Computation specific to a rate measure type

        M_avg becomes M_rate
        max/min are computed on M_rates, not on values

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
        avg_suffix: str = '_rate',
    ):
        """ generate deltaValues from ObsMeteor.data """
        # force avg to be computed
        my_measure['avg'] = True
        super(ProcessJsonDataRate, self).loadData(
            my_measure,
            json_file_data,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            trace_flag,
            False,
            '_rate'
        )

    def loadMaxMin(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        tracing_flag: bool = False,
        b_use_rate: bool = False,
    ):
        super(ProcessJsonDataRate, self).loadMaxMin(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            tracing_flag,
            True,
        )
