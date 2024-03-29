from app.tools.aggTools import calcAggDate
# from app.classes.calcul.calcObservation import CalcObs
# from app.classes.calcul.calcAggreg import CalcAggreg
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.jsonPlus import JsonPlus
from app.tools.telemetry import Telemetry
import os
import app.tools.myTools as t


class CalcTestEngine():
    def __init__(self, *args, **kwargs):
        # self.calc = AllCalculus()
        # self.calc_obs = CalcObs.GetInstance()
        # self.calc_agg = CalcAggreg()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_name = os.path.join(base_dir, '../fixtures/calculus_test_suite.json')
        texte = ''

        with open(file_name, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)
            self.my_test_suite = JsonPlus().loads(texte)

    def run_test(self, name, option: int = 255):
        """
            Run all tests in our suite test

            option:
                1: load Obs
                3: load Aggregations
                7: load extremeFix
        """
        try:
            self.tracer = Telemetry.Start("calculus", name)
            pid = PosteMetier.getPosteIdByMeteor('BBF015')
            if pid is None:
                p = PosteMetier(1)
                p.data.meteor = 'BBF015'
                p.data.fuseau = 4
                p.save()
            for a_test in self.my_test_suite:
                if a_test['name'] != name:
                    continue
                # prepare our full json
                my_json = JsonPlus().loads("""
                    {
                        "meteor" : "BBF015",
                        "info" : {
                            "blabla": "blabla"
                        },
                        "data": []
                    }
                    """)
                j_data = a_test['data']
                my_json['data'] = j_data
                # # remove any existing data
                # self.calc.delete_obs_agg(True)

                if ((option & 1) == 1):
                    my_params = {"param": {
                        "json": my_json,
                        "trace_flag": False,
                        "is_tmp": True,
                        "validation": False,
                        "filename": 'test_json',
                    }}
                    self.calc_obs.LoadJsonControler(my_params)

                if ((option & 2) == 2):
                    self.calc_agg._computeAggreg(True, False)

                error_msg = []
                # load list of resultset to load
                for a_result in a_test['results']:
                    b_compute_agg_date = False
                    if a_result['t'] == "A" or a_result['t'] == "AT":
                        test_dat = "1900-12-31T00:00:00"
                    elif a_result.__contains__('dat'):
                        test_dat = a_result['dat']
                    elif a_result.__contains__('idx'):
                        test_dat = j_data[a_result['idx']]['stop_dat']
                        b_compute_agg_date = True
                    elif a_result.__contains__('count'):
                        test_dat = '1900-12-31T00:00:00+00:00'
                    else:
                        raise Exception('calTestEngine', 'wrong test JSON file')

                    if a_result["t"] == "O":
                        my_row = ObsMeteor(pid, test_dat, True)
                    else:
                        # if idx is given, need to compute agregation date for the level
                        if b_compute_agg_date is True:
                            test_dat = calcAggDate('H', test_dat, 0, True)
                            hour_deca = 0
                            if a_result.__contains__('hour_deca') is True:
                                hour_deca = a_result['hour_deca']
                            test_dat = calcAggDate(a_result["t"], test_dat, hour_deca, False)
                        my_row = AggMeteor(pid, a_result['t'], test_dat)

                    # if a_result['t'] == "O":
                    #     t.logdebug('obs: ' + str(my_row.data.id) + ", dat: " + str(my_row.data.stop_dat) + ", j: " + JsonPlus().dumps(my_row.data.j))
                    # else:
                    #     t.logdebug('agg_' + a_result['t'] + ': ' + str(my_row.data.id) + ", dat: " + str(my_row.data.start_dat) + ", j: " + JsonPlus().dumps(my_row.data.j))
                    if a_result.__contains__('count'):
                        stop_dat_mask = ''
                        if a_result.__contains__('stop_dat_mask'):
                            stop_dat_mask = a_result['stop_dat_mask']
                        if a_result['t'] == 'O':
                            my_count = my_row.count(pid, stop_dat_mask, True)
                        else:
                            my_count = my_row.count(a_result['t'], pid, stop_dat_mask)
                        assert my_count == a_result['count']
                        continue

                    # check the result
                    for k in a_result.items():
                        if k[0] == 't' or k[0] == 'idx' or k[0] == 'dat':
                            continue

                        if a_result[k[0]] != my_row.data.j[k[0]]:
                            err_txt = "t: " + a_result['t'] + ', key:' + k[0]
                            err_txt = err_txt + ' -> ' + str(my_row.data.j[k[0]]) + ' should be ' + str(a_result[k[0]])
                            t.logError("error: " + str(err_txt))
                            error_msg.append(err_txt)

            assert error_msg.__len__() == 0

        except Exception as inst:
            t.logdebug(inst.with_traceback(None))
            assert "error in " == " json file"
