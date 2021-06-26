from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.calcul.observation.processJsonData import ProcessJsonData
from app.tools.aggTools import isFlagged
from app.tools.climConstant import MeasureProcessingBitMask
import json
import datetime


class ProcessJsonDataAvg(ProcessJsonData):
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
        """
            loadObservationDatarow

            load Observation dataRow from json measures

            load delta_values from json mesures
        """
        obs_j = obs_meteor.data.j

        if my_measure['target_key'] == 'barometer':
            my_value_avg = my_values.get(target_key + '_a')

        my_value_avg = my_values.get(target_key + '_a')
        my_value_instant = my_values.get(target_key + '_i')
        my_value_dir = my_values.get(target_key + '_di')
        tmp_duration = my_values.get(target_key + '_du')
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            tmp_duration = 60
        if my_value_avg is None:
            if my_value_instant is None:
                return
            else:
                my_value_avg = my_value_instant

        # get our value to aggregate
        if my_measure.__contains__('measureType'):
            if my_measure['measureType'] == 'inst':
                # for omm measure...
                my_value_aggreg = my_value_instant
            else:
                my_value_aggreg = my_value_avg
        else:
            if my_value_instant is not None:
                my_value_aggreg = my_value_instant

        tmp_s = my_value_aggreg * tmp_duration

        if my_value_aggreg is None:
            # no data suitable for us
            return

        # get current values from our aggregations
        tmp_s_old = tmp_duration_old = 0
        if obs_j.get(target_key + '_s') is not None:
            tmp_s_old = obs_j[target_key + '_s']
            if tmp_s == tmp_s_old:
                # no change on avg computation
                return
            tmp_duration_old = obs_j.get(target_key + '_duration')
            if tmp_duration_old is None:
                tmp_duration_old = tmp_duration
            if tmp_duration != tmp_duration_old:
                raise('loadDataInObs', 'duration mitchmath for ' + target_key + ': in obs' + str(tmp_duration_old) + ', in json: ' + str(tmp_duration))
            delta_values[target_key + '_s_old'] = tmp_s_old
            delta_values[target_key + '_duration_old'] = tmp_duration_old

        # save data in dv
        delta_values[target_key + '_s'] = tmp_s
        delta_values[target_key + '_duration'] = tmp_duration

        # save data in obs
        obs_j[target_key] = my_value_aggreg

        if my_value_dir is not None:
            obs_j[target_key + '_dir'] = my_value_dir
