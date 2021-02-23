from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
import datetime
from app.classes.metier.posteMetier import PosteMetier
from app.tools.jsonPlus import JsonPlus
from app.classes.typeInstruments.typeTemp import TypeTemp
from app.classes.calcul.avgCompute import avgCompute
import json


class type_temp_test():
    """ debug helper """

    def __init__(self):
        """ pre load std data """
        self.dt_test = datetime.datetime(
            2021, 2, 11, 13, 9, 30, 0, datetime.timezone.utc)
        self.p_test = PosteMetier(1)

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
        json_string2 = """
{
  "meteor" : "BBF015",
  "info" :
  {
    "title":"MÃ©tÃ©o en direct",
    "location":"Bain Boeuf, Cap Malheureux / Maurice",
    "time":"23/02/2021 Ã  08h40",
    "lat":"19&deg; 59.22' S",
    "lon":"057&deg; 36.30' E",
    "alt":"40 mÃ¨tres",
    "hardware":"Vantage Pro2",
    "uptime":"107 jours, 16 heures, 57 minutes",
    "serverUptime":"107 jours, 16 heures, 57 minutes",
    "weewxVersion":"3.9.2",
    "monitors": {
      "signal_quality": "100",
      "txBatteryStatus": "OK",
      "consBatteryVoltage" : "4.8"
    }
  },
  "data":
  [
      {
          "current":
          {
              "dat" : "2021-02-11T08:35:00+00:00",
              "duration" : 300,
              "out_temp":"28.1",
              "windchill":"28.1",
              "heatindex":"32.4",
              "dewpoint":"24.5",
              "humidity":"81",
              "in_humidity":"65",
              "barometer":"1014.6",
              "wind":"1.2",
              "wind_dir":"90",
              "wind_max":"0",
              "wind_max_dir":"95",
              "rain_rate":"0.0",
              "rain":"0.0",
              "uv_indice":"3.3",
              "etp":"0.0",
              "solar_radiation":"536",
              "in_temp":"29.2",
              "rx": "100",
              "voltage" : "4.8"
          },
          "aggregations":
          [
              {
                  "level" : "D",
                  "out_temp_max":"28.1",
                  "out_temp_max_time":"2021-02-11T08:39:00+00:00",
                  "out_temp_min":"24.7",
                  "out_temp_min_time":"2021-02-11T06:35:00+00:00",
                  "out_temp_avg":"26.3",
                  "heatindex_max":"32.6",
                  "heatindex_max_time":"2021-02-11T08:39:00+00:00",
                  "windchill_min":"24.7",
                  "windchill_min_time":"2021-02-11T06:35:00+00:00",
                  "humidity_max":"91",
                  "humidity_max_time":"2021-02-11T07:15:00+00:00",
                  "humidity_min":"80",
                  "humidity_min_time":"2021-02-11T00:00:00+00:00",
                  "dewpoint_max":"24.9",
                  "dewpoint_max_time":"2021-02-11T08:37:00+00:00",
                  "dewpoint_min":"22.8",
                  "dewpoint_min_time":"2021-02-11T06:35:00+00:00",
                  "barometer_max":"1014.6",
                  "barometer_mx_time":"2021-02-11T08:30:00+00:00",
                  "barometer_min":"1012.6",
                  "barometer_min_time":"2021-02-11T04:22:00+00:00",
                  "rain":"1.2",
                  "rain_rate_max":"1.8",
                  "rain_rate_max_time":"2021-02-11T06:16:00+00:00",
                  "wind_max":"0",
                  "wind_max_dir":"92",
                  "wind_max_time":"2021-02-11T00:00:00+00:00",
                  "wind_avg":"0",
                  "uv_indice_max":"3.4",
                   "uv_indice_max_time":"2021-02-11T08:38:00+00:00",
                   "etp_sum":"0.1",
                   "radiation_max":"664",
                   "radiation_max_time":"2021-02-11T08:27:00+00:00",
                   "radiation_min":"0",
                   "radiation_min_time":"2021-02-11T00:00:00+00:00",
                   "rx_max":"100",
                   "rx_max_time":"2021-02-11T03:20:00+00:00",
                   "rx_min":"94",
                   "rx_min_time":"2021-02-11T00:10:00+00:00",
                   "voltage_max":"4.8",
                   "voltage_max_time":"2021-02-11T00:00:00+00:00",
                   "voltage_min":"2.9",
                   "voltage_min_time":"2021-02-11T01:56:00+00:00",
                   "in_temp_max":"29.2",
                   "in_temp_max_time":"2021-02-11T08:36:00+00:00",
                   "in_temp_min":"26.0",
                   "in_temp_min_time":"2021-02-11T05:50:00+00:00"
              }
          ]
      },
      {
        "current" :
        {
            "dat" : "2021-02-11T08:40:00+00:00",
            "duration" : 300 ,
            "out_temp":"28.4",
            "windchill":"28.4",
            "heatindex":"32.9",
            "dewpoint":"24.4",
            "humidity":"79",
            "in_humidity":"65",
            "barometer":"1014.5",
            "wind":"0",
            "wind_dir":"90",
            "wind_max":"0",
            "wind_max_dir":"95",
            "rain_rate":"0.0",
            "rain":"0.0",
            "uv_indice":"3.6",
            "etp":"0.0",
            "solar_radiation":"547",
            "in_temp":"29.3",
            "rx": "100",
            "voltage" : "4.8"
        },
        "aggregations" :
        [
            {
                "level" : "D",
                "out_temp_max":"28.4",
                "out_temp_max_time":"2021-02-11T08:44:00+00:00",
                "out_temp_min":"24.7",
                "out_temp_min_time":"2021-02-11T06:35:00+00:00",
                "out_temp_avg":"26.3",
                "heatindex_max":"33.1",
                "heatindex_max_time":"2021-02-11T08:44:00+00:00",
                "windchill_min":"24.7",
                "windchill_min_time":"2021-02-11T06:35:00+00:00",
                "humidity_max":"91",
                "humidity_max_time":"2021-02-11T07:15:00+00:00",
                "humidity_min":"79",
                "humidity_min_time":"2021-02-11T08:44:00+00:00",
                "dewpoint_max":"24.9",
                "dewpoint_max_time":"2021-02-11T08:37:00+00:00",
                "dewpoint_min":"22.8",
                "dewpoint_min_time":"2021-02-11T06:35:00+00:00",
                "barometer_max":"1014.6",
                "barometer_mx_time":"2021-02-11T08:30:00+00:00",
                "barometer_min":"1012.6",
                "barometer_min_time":"2021-02-11T04:22:00+00:00",
                "rain":"1.2",
                "rain_rate_max":"1.8",
                "rain_rate_max_time":"2021-02-11T06:16:00+00:00",
                "wind_max":"0",
                "wind_max_dir":"92",
                "wind_max_time":"2021-02-11T00:00:00+00:00",
                "wind_avg":"0",
                  "uv_indice_max":"3.7",
                 "uv_indice_max_time":"2021-02-11T08:44:00+00:00",
                 "etp_sum":"0.1",
                 "radiation_max":"664",
                 "radiation_max_time":"2021-02-11T08:27:00+00:00",
                 "radiation_min":"0",
                 "radiation_min_time":"2021-02-11T00:00:00+00:00",
                 "rx_max":"100",
                 "rx_max_time":"2021-02-11T03:20:00+00:00",
                 "rx_min":"94",
                 "rx_min_time":"2021-02-11T00:10:00+00:00",
                 "voltage_max":"4.8",
                 "voltage_max_time":"2021-02-11T00:00:00+00:00",
                 "voltage_min":"2.9",
                 "voltage_min_time":"2021-02-11T01:56:00+00:00",
                 "in_temp_max":"29.3",
                 "in_temp_max_time":"2021-02-11T08:44:00+00:00",
                 "in_temp_min":"26.0",
                 "in_temp_min_time":"2021-02-11T05:50:00+00:00"
            }
        ]
      },
      {
          "current" :
          {
              "dat" : "2021-02-11T08:45:00+00:00",
              "duration" : 300,
              "out_temp":"28.6",
              "windchill":"28.6",
              "heatindex":"33.1",
              "dewpoint":"24.2",
              "humidity":"77",
              "in_humidity":"65",
              "barometer":"1014.4",
              "wind":"0",
              "wind_dir":"90",
              "wind_max":"0",
              "wind_max_dir":"95",
              "rain_rate":"0.0",
              "rain":"0.0",
              "uv_indice":"3.7",
              "etp":"0.0",
              "solar_radiation":"578",
              "in_temp":"29.3",
              "rx": "100",
              "voltage" : "4.8"
          },
          "aggregations" :
          [
              {
                  "level" : "D",
                  "out_temp_max":"28.6",
                  "out_temp_max_time":"2021-02-11T08:50:00+00:00",
                  "out_temp_min":"24.7",
                  "out_temp_min_time":"2021-02-11T06:35:00+00:00",
                  "out_temp_avg":"26.3",
                  "heatindex_max":"33.3",
                  "heatindex_max_time":"2021-02-11T08:46:00+00:00",
                  "windchill_min":"24.7",
                  "windchill_min_time":"2021-02-11T06:35:00+00:00",
                  "humidity_max":"91",
                  "humidity_max_time":"2021-02-11T07:15:00+00:00",
                  "humidity_min":"77",
                  "humidity_min_time":"2021-02-11T08:49:00+00:00",
                  "dewpoint_max":"24.9",
                  "dewpoint_max_time":"2021-02-11T08:37:00+00:00",
                  "dewpoint_min":"22.8",
                  "dewpoint_min_time":"2021-02-11T06:35:00+00:00",
                  "barometer_max":"1014.6",
                  "barometer_mx_time":"2021-02-11T08:30:00+00:00",
                  "barometer_min":"1012.6",
                  "barometer_min_time":"2021-02-11T04:22:00+00:00",
                  "rain":"1.2",
                  "rain_rate_max":"1.8",
                  "rain_rate_max_time":"2021-02-11T06:16:00+00:00",
                  "wind_max":"0",
                  "wind_max_dir":"92",
                  "wind_max_time":"2021-02-11T00:00:00+00:00",
                  "wind_avg":"0",
                  "uv_indice_max":"3.9",
                   "uv_indice_max_time":"2021-02-11T08:47:00+00:00",
                   "etp_sum":"0.1",
                   "radiation_max":"664",
                   "radiation_max_time":"2021-02-11T08:27:00+00:00",
                   "radiation_min":"0",
                   "radiation_min_time":"2021-02-11T00:00:00+00:00",
                   "rx_max":"100",
                   "rx_max_time":"2021-02-11T03:20:00+00:00",
                   "rx_min":"94",
                   "rx_min_time":"2021-02-11T00:10:00+00:00",
                   "voltage_max":"4.8",
                   "voltage_max_time":"2021-02-11T00:00:00+00:00",
                   "voltage_min":"2.9",
                   "voltage_min_time":"2021-02-11T01:56:00+00:00",
                   "in_temp_max":"29.4",
                   "in_temp_max_time":"2021-02-11T08:49:00+00:00",
                   "in_temp_min":"26.0",
                   "in_temp_min_time":"2021-02-11T05:50:00+00:00"
              }
          ]
      }
    ]
  }
        """
        self.j_test = JsonPlus().loads(json_string)
        self.j2_test = JsonPlus().loads(json_string2)

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()

    def loadObs(self):
        return self.loadObsCommon(self.j_test)

    def loadObs2(self):
        return self.loadObsCommon(self.j2_test)

    def loadObsCommon(self, m_j: json):
        try:
            tt = TypeTemp()
            # tt.mapping[0] -> first measure, tt.p_test, tt_o_test, tt.j_test, tt.a_test

            pp = PosteMetier(1)
            # remove existing exclusion in poste (will require a reload)
            xx = pp.exclus
            pp.exclus = []

            # call the method to update obs, and return delta_val
            ma = avgCompute()
            result = []
            for my_measure in tt.mesures:
                delta_val = ma.updateObsAndGetDelta(self.p_test, my_measure, m_j, 0, self.o_test, True)
                result.append(delta_val)

            # restore exclus, as our object is cached
            pp.exclus = xx

            # example of test to execute
            # Observation values should be tested too...

            if m_j['data'].__len__() == 2:
                # delta_val validation
                if int(result[0]['out_temp_sum']) != 8850:
                    return "out_temp_sum wrong " + str(result[0]['out_temp_sum'])
                if int(result[0]['out_temp_duration']) != 300:
                    return "out_temp_duration wrong: " + str(result[0]['out_temp_duration'])
                if float(result[0]['out_temp_max']) != 29.5:
                    return "out_temp_max wrong: " + str(result[0]['out_temp_max'])
                if str(result[0]['out_temp_max_time']) != '2021-02-11 13:12:00+00:00':
                    return "out_temp_max_time wrong: " + str(result[0]['out_temp_max_time'])
                if float(result[0]['out_temp_min']) != 29.5:
                    return "out_temp_min wrong: " + str(result[0]['out_temp_min'])
                if str(result[0]['out_temp_min_time']) != '2021-02-11 13:12:00+00:00':
                    return "out_temp_min_time wrong: " + str(result[0]['out_temp_min_time'])
            else:
                print('todo')

            # return to the browser when executed in interactive mode... (not needed in real testing situation)
            return result

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def loadObsAndAgg(self):
        try:
            tt = TypeTemp()
            # tt.mapping[0] -> first measure, tt.p_test, tt_o_test, tt.j_test, tt.a_test

            pp = PosteMetier(1)
            # remove existing exclusion in poste (will require a reload)
            xx = pp.exclus
            pp.exclus = []

            # call the method to update obs, and return delta_val
            ma = avgCompute()
            delta_val = ma.updateObsAndGetDelta(self.p_test, tt.mapping[0], self.j_test, 0, self.o_test, True)
            # agg_recompute = ma.update_aggs(self.p_test, tt.mapping[0], self.j_test, 0, self.a_test, delta_val, True)

            # restore exclus, as our object is cached
            pp.exclus = xx

            # return to the browser when executed in interactive mode... (not needed in real testing situation)
            # return agg_recompute
            return delta_val

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
