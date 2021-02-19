from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
import datetime
from app.classes.posteMeteor import PosteMeteor
from app.tools.jsonPlus import jsonPlus
from app.classes.typeInstruments.typeTemp import TypeTemp
from app.classes.measures.measureAvg import MeasureAvg
from app.tools.getterSetter import GetterSetter


class type_temp_test():
    """ debug helper """

    def __init__(self):
        """ pre load std data """
        self.dt_test = datetime.datetime(
            2021, 2, 11, 13, 9, 30, 0, datetime.timezone.utc)
        self.p_test = PosteMeteor(1)

        self.o_test = self.p_test.observation(self.dt_test)
        self.a_test = self.p_test.aggregations(self.dt_test)
        json_string = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {
                    "current":
                        {
                            "dat" : "2021-02-11T13:09:30+00:00",
                            "duration" : 300,
                            "out_temp" : 29.5
                        },
                    "aggregations": [
                        {
                            "level" : "H",
                            "out_temp_avg" : 32.75
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                },
                {
                    "current" :
                        {
                            "dat" : "2021-02-11T13:09:40+00:00",
                            "duration" : 300,
                            "out_temp" : 30
                        },
                    "aggregations" : [
                        {
                            "level" : "H",
                            "out_temp_avg" : 33
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                }
            ]
        }
        """
        self.j_test = jsonPlus().loads(json_string)

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()

    def getset(self):
        """ getter/setter test on djamgo objects """
        fm = GetterSetter()
        old_meteor = fm.get(self.p_test, 'meteor')
        ret = {'meteor': old_meteor}
        fm.set(self.p_test, 'new value', 'meteor')
        ret['first'] = str(self.p_test.data)
        fm.set(self.p_test, old_meteor, 'meteor')
        ret['second'] = str(self.p_test.data)
        return ret

    def load_obs(self):
        try:
            tt = TypeTemp()
            # tt.mapping[0] -> first measure, tt.p_test, tt_o_test, tt.j_test, tt.a_test

            pp = PosteMeteor(1)
            # remove existing exclusion in poste (will require a reload)
            xx = pp.exclus
            pp.exclus = []

            # call the method to update obs, and return delta_val
            ma = MeasureAvg()
            delta_val = ma.update_obs_and_get_delta(
                self.p_test, tt.mapping[0], self.j_test, 0, self.o_test, True)

            # restore exclus, as our object is cached
            pp.exclus = xx

            # example of test to execute
            # Observation values should be tested too...

            # delta_val validation
            if int(delta_val['out_temp_sum']) != 8850:
                return "out_temp_sum wrong " + str(delta_val['out_temp_sum'])
            if int(delta_val['out_temp_duration']) != 300:
                return "out_temp_duration wrong: " + str(delta_val['out_temp_duration'])
            if float(delta_val['out_temp_max']) != 29.5:
                return "out_temp_max wrong: " + str(delta_val['out_temp_max'])
            if str(delta_val['out_temp_max_time']) != '2021-02-11 13:12:00+00:00':
                return "out_temp_max_time wrong: " + str(delta_val['out_temp_max_time'])
            if float(delta_val['out_temp_min']) != 29.5:
                return "out_temp_min wrong: " + str(delta_val['out_temp_min'])
            if str(delta_val['out_temp_min_time']) != '2021-02-11 13:12:00+00:00':
                return "out_temp_min_time wrong: " + str(delta_val['out_temp_min_time'])

            # return to the browser when executed in interactive mode... (not needed in real testing situation)
            return delta_val

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def load_agg(self):
        try:
            tt = TypeTemp()
            # tt.mapping[0] -> first measure, tt.p_test, tt_o_test, tt.j_test, tt.a_test

            pp = PosteMeteor(1)
            # remove existing exclusion in poste (will require a reload)
            xx = pp.exclus
            pp.exclus = []

            # call the method to update obs, and return delta_val
            ma = MeasureAvg()
            delta_val = ma.update_obs_and_get_delta(
                self.p_test, tt.mapping[0], self.j_test, 0, self.o_test, True)
            agg_recompute = ma.update_aggs(
                self.p_test, tt.mapping[0], self.j_test, 0, self.a_test, delta_val, True)

            # restore exclus, as our object is cached
            pp.exclus = xx

            # return to the browser when executed in interactive mode... (not needed in real testing situation)
            return agg_recompute

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
