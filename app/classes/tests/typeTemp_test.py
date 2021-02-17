from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
import datetime
from dateutil.relativedelta import relativedelta
from app.classes.obsMeteor import ObsMeteor
from app.classes.posteMeteor import PosteMeteor
from app.classes.ExcluMeteor import ExcluMeteor
from app.tools.agg_tools import get_agg_object
import json
from app.tools.jsonPlus import jsonPlus
from app.classes.typeInstruments.typeTemp import TypeTemp
from app.classes.measures.measureAvg import MeasureAvg

class type_temp_test():
    """ debug helper """

    def __init__(self):
        """ pre load std data """
        self.dt_test = datetime.datetime(2021, 2, 11, 13, 9, 30, 0, datetime.timezone.utc)
        self.p_test = PosteMeteor.get(1)

        self.o_test = self.p_test.observation(self.dt_test)
        self.a_test = self.p_test.aggregations(self.dt_test)
        json_string = """
        {
            "metor" : "BBF015",
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
                            "temp_out" : 29.5
                        },
                    "aggregations": [
                        {
                            "level" : "H",
                            "temp_out_avg" : 32.75
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
                            "temp_out" : 30
                        },
                    "aggregations" : [
                        {
                            "level" : "H",
                            "temp_out_avg" : 33
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

    def load_obs(self):
        try:
            tt = TypeTemp()
            # tt.mapping[0] -> first measure
            ma = MeasureAvg()
            ma.update_obs_and_get_delta(self.p_test, tt.mapping[0], self.j_test, 0, self.o_test, True)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,


if __name__ == "__main__":
    try:
        ma = MeasureAvg()
        ma.load_obs()

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
