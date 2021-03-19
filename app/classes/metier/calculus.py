from app.classes.repository.posteMeteor import PosteMeteor
from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
from app.classes.metier.posteMetier import PosteMetier
from app.classes.metier.typeInstrumentAll import TypeInstrumentAll
from app.tools.jsonPlus import JsonPlus
import json


class Calculus():

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()

    def run(self, m_j: json, b_serialize: bool, flag: bool = True) -> json:
        try:
            all_instr = TypeInstrumentAll()
            ret = []
            if b_serialize:
                self.delete_obs_agg()

            idx = 0
            while idx < m_j['data'].__len__():
                pid = PosteMeteor.getPosteIdByMeteor(m_j['meteor'])
                if pid is None:
                    raise Exception('doCalculus', 'unknown code meteor: ' + m_j['meteor'])
                self.p_test = PosteMetier(pid)
                self.o_test = self.p_test.observation(m_j['data'][idx]['current']['dat'])
                if self.o_test.data.duration == 0:
                    self.o_test.data.duration = m_j['data'][idx]['current']['duration']
                self.a_test = self.p_test.aggregations(m_j['data'][idx]['current']['dat'], m_j['data'][idx]['current']['duration'])

                # call the method to update obs, and return delta_val
                all_instr.process_json(self.p_test, m_j, idx, self.o_test, self.a_test)

                if b_serialize:
                    # self.o_test.data.j['dv'] = {}
                    self.o_test.save()
                    for i in (0, 1, 2, 3, 4, 5, 6):
                        # self.a_test[i].data.j['dv'] = {}
                        self.a_test[i].save()
                # else:
                # will return to the caller when in test mode
                if idx == 0:
                    helper = ' - cut and paste this data into https://codebeautify.org/jsonviewer'
                else:
                    helper = ''
                ret.append({
                    'info': 'idx=' + str(idx) + helper,
                    'dat': m_j['data'][idx]['current']['dat'],
                    'observation': JsonPlus().loads(JsonPlus().dumps(self.o_test.data.j)),
                    'agg_hour': {'start_dat': self.a_test[0].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[0].data.j))},
                    'agg_day': {'start_dat': self.a_test[1].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[1].data.j))},
                    'agg_month': {'start_dat': self.a_test[2].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[2].data.j))},
                    'agg_year': {'start_dat': self.a_test[3].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[3].data.j))},
                    'agg_all': {'start_dat': self.a_test[4].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[4].data.j))},
                    'agg_day before': {'start_dat': self.a_test[5].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[5].data.j))},
                    'agg_day after': {'start_dat': self.a_test[6].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.a_test[6].data.j))},
                    }
                )

                idx += 1

            return ret

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            ret.append({'Exception': inst.__str__()})
            return ret
