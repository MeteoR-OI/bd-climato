from app.tools.aggTools import calcAggDate
from app.classes.integrationTests.typeTemp import TypeTempTest
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.jsonPlus import JsonPlus
import os
import logging


class CalcTestEngine():
    def __init__(self, *args, **kwargs):
        self.tt = TypeTempTest()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_name = os.path.join(base_dir, '../fixtures/calculus_test_suite.json')
        texte = ''

        with open(file_name, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)
            self.my_test_suite = JsonPlus().loads(texte)

    def run_test(self, name):
        """
            Run all tests in our suite test
        """
        try:
            pid = PosteMetier.getPosteIdByMeteor('BBF015')
            if pid is None:
                p = PosteMetier(1)
                p.data.meteor = 'BBF015'
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
                # remove any existing data
                self.tt.delete_obs_agg()

                self.tt.doCalculus(my_json, True)

                # check our results
                result_set = {
                    "O": [],
                    "H": [],
                    "D": [],
                    "M": [],
                    "Y": [],
                    "A": [],
                }
                # load list of resultset to load
                for a_result in a_test['results']:
                    if a_result.__contains__('idx'):
                        result_set[a_result['t']].append(j_data[a_result['idx']]['current']['stop_dat'])
                    # elif a_result.__contains__('count'):
                    #     result_set[a_result['t']].append('count')
                    else:
                        raise Exception('calTestEngine', 'wrong test JSON file')

                error_msg = []
                # load list of resultset to load
                for a_result in a_test['results']:
                    obs_stop_dat = j_data[a_result['idx']]['current']['stop_dat']
                    if a_result["t"] == "O":
                        my_row = ObsMeteor(pid, obs_stop_dat)
                        if a_result.__contains__('count'):
                            stop_dat_mask = ''
                            if a_result.__contains__('stop_dat_mask'):
                                stop_dat_mask = a_result['stop_dat_mask']
                            my_count = my_row.count(pid, stop_dat_mask)
                            assert my_count == a_result['count']
                            continue
                    else:
                        agg_start_dat = calcAggDate('H', obs_stop_dat, 0, True)
                        hour_deca = 0
                        if a_result.__contains__('hour_deca') is True:
                            hour_deca = a_result['hour_deca']
                        agg_start_dat = calcAggDate(a_result["t"], agg_start_dat, hour_deca, False)
                        my_row = AggMeteor(pid, a_result['t'], agg_start_dat)
                        if a_result.__contains__('count'):
                            stop_dat_mask = ''
                            if a_result.__contains__('stop_dat_mask'):
                                stop_dat_mask = a_result['stop_dat_mask']
                            my_count = my_row.count(a_result['t'], pid, stop_dat_mask)
                            assert my_count == a_result['count']
                            continue

                    # check the result
                    for k in a_result.items():
                        if k[0] == 't' or k[0] == 'idx':
                            continue

                        if a_result[k[0]] != my_row.data.j[k[0]]:
                            err_txt = "t: " + a_result['t'] + ', idx: ' + str(a_result['idx']) + ', key:' + k[0]
                            err_txt = err_txt + ' -> ' + str(my_row.data.j[k[0]]) + ' should be ' + str(a_result[k[0]])
                            logging.error("error: " + str(err_txt))
                            error_msg.append(err_txt)

            assert error_msg.__len__() == 0

        except Exception as inst:
            print(inst.with_traceback(None))
            assert "error in " == " json file"
