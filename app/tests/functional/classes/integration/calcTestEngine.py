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
                    result_set[a_result['t']].append(j_data[a_result['idx']]['current']['stop_dat'])

                error_msg = []
                # load list of resultset to load
                for a_result in a_test['results']:
                    if a_result["t"] == "O":
                        tmp_o = ObsMeteor(pid, j_data[a_result['idx']]['current']['stop_dat'])
                        for k in a_result.items():
                            if k[0] == 't' or k[0] == 'idx':
                                continue
                            if a_result[k[0]] != tmp_o.data.j[k[0]]:
                                err_txt = "t: " + a_result['t'] + ', idx: ' + str(a_result['idx']) + ', key:' + k[0]
                                err_txt = err_txt + ' -> ' + str(tmp_o.data.j[k[0]]) + ' should be ' + str(a_result[k[0]])
                                logging.error("error: " + str(err_txt))
                                error_msg.append(err_txt)

            assert error_msg.__len__() == 0

        except Exception as inst:
            print(inst.with_traceback(None))
            assert "error in " == " json file"
