from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.observation.processJsonData import ProcessJsonData
from app.tools.aggTools import isFlagged, loadFromExclu, calcAggDate, delKey
import json


class ProcessJsonDataNo(ProcessJsonData):
    """
        ProcessJsonDataNo

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
        avg_suffix: str = '_avg',
    ):
        return

    def getDeltaFromObservation(self, my_measure: json, obs_meteor: ObsMeteor, json_key: str, delta_values: json) -> json:
        """
            getDeltaFromObs

            susbtract M_sum and M_duration
        """
        return
