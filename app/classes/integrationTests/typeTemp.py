from app.classes.repository.posteMeteor import PosteMeteor
from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
import datetime
from app.classes.metier.posteMetier import PosteMetier
from app.classes.metier.typeInstrumentAll import TypeInstrumentAll
from app.tools.jsonPlus import JsonPlus
import json


class TypeTempTest():
    """ debug helper """

    def __init__(self):
        """ pre load std data """
        self.dt_test = datetime.datetime(2021, 2, 11, 13, 9, 30, 0, datetime.timezone.utc)
        self.p_test = PosteMetier(1)

        self.o_test = self.p_test.observation(self.dt_test)
        self.a_test = self.p_test.aggregations(self.dt_test, 5)
        json_string0 = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {"current" : {"dat" : "2021-02-11T13:30:00+00:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"dat" : "2021-02-11T13:01:00+00:00", "duration" : 5, "out_temp" : 10}},
                {"current" : {"dat" : "2021-02-11T13:35:00+00:00", "duration" : 5, "out_temp" : 30}}
            ]
        }
        """
        json_string1 = """
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
                            "duration" : 5,
                            "out_temp" : 29.5
                        },
                    "aggregations": [
                        {
                            "level" : "H",
                            "out_temp_avg" : 32.75,
                            "out_temp_duration": 5
                        },
                        {
                            "level" : "D",
                            "out_temp_avg" : 33,
                            "out_temp_duration": 25
                        }
                    ]
                },
                {
                    "current" :
                        {
                            "dat" : "2021-02-11T13:09:40+00:00",
                            "duration" : 5,
                            "out_temp" : 32
                        },
                    "aggregations" : [
                        {
                            "level" : "H",
                            "out_temp_avg" : 33,
                            "out_temp_duration": 10
                        },
                        {
                            "level" : "D",
                            "out_temp_avg" : 20
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
                    "duration" : 5,
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
                        "barometer_max_time":"2021-02-11T08:30:00+00:00",
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
                    "duration" : 5 ,
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
                        "barometer_max_time":"2021-02-11T08:30:00+00:00",
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
                    "duration" : 5,
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
                        "barometer_max_time":"2021-02-11T08:30:00+00:00",
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
        json_string3 = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {"current":      {"dat" : "2021-01-30T05:45:00+00:00", "duration" : 5, "out_temp" : 25.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T05:50:00+00:00", "duration" : 5, "out_temp" : 25.3}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T05:55:00+00:00", "duration" : 5, "out_temp" : 25.6}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T06:00:00+00:00", "duration" : 5, "out_temp" : 25.9}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:05:00+00:00", "duration" : 5, "out_temp" : 26.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:10:00+00:00", "duration" : 5, "out_temp" : 26.1}, "aggregations": [
                                                                                        {"level" : "D", "out_temp_avg" : 26.9} ]},
                {"current":      {"dat" : "2021-01-31T06:15:00+00:00", "duration" : 5, "out_temp" : 26.5}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:20:00+00:00", "duration" : 5, "out_temp" : 26.6}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:10:00+00:00", "duration" : 5, "out_temp" : 24.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:15:00+00:00", "duration" : 5, "out_temp" : 24.4}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:20:00+00:00", "duration" : 5, "out_temp" : 24.8}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:25:00+00:00", "duration" : 5, "out_temp" : 25.2}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:30:00+00:00", "duration" : 5, "out_temp" : 25.6}, "aggregations": [ ]}
            ]
        }
        """
        json_string4 = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {"current":      {"dat" : "2021-01-30T05:45:00+00:00", "duration" : 5, "out_temp" : 25.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T05:50:00+00:00", "duration" : 5, "out_temp" : 25.3}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T05:55:00+00:00", "duration" : 5, "out_temp" : 25.7}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-30T06:00:00+00:00", "duration" : 5, "out_temp" : 26.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:05:00+00:00", "duration" : 5, "out_temp" : 25.5}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:10:00+00:00", "duration" : 5, "out_temp" : 25.4}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:15:00+00:00", "duration" : 5, "out_temp" : 24.5}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-01-31T06:20:00+00:00", "duration" : 5, "out_temp" : 25.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:10:00+00:00", "duration" : 5, "out_temp" : 24.0}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:15:00+00:00", "duration" : 5, "out_temp" : 24.4}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:20:00+00:00", "duration" : 5, "out_temp" : 24.8}, "aggregations": [ ]},
                {"current":      {"dat" : "2021-02-01T10:25:00+00:00", "duration" : 5, "out_temp" : 24.7}, "aggregations": [
                                     {"level" : "D", "out_temp_max" : 25.0, "out_temp_max_time" : "2021-02-01T10:27:35+00:00"} ]},
                {"current":      {"dat" : "2021-02-01T10:30:00+00:00", "duration" : 5, "out_temp" : 24.7}, "aggregations": [ ]}
            ]
        }
        """
        self.j0_test = JsonPlus().loads(json_string0)
        self.j1_test = JsonPlus().loads(json_string1)
        self.j2_test = JsonPlus().loads(json_string2)
        self.j3_test = JsonPlus().loads(json_string3)
        self.j4_test = JsonPlus().loads(json_string4)

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()

    def doCalculusJ0(self):
        return self.doCalculus(self.j0_test, True)

    def doCalculusJ1(self):
        return self.doCalculus(self.j1_test, True)

    def doCalculusJ2(self):
        return self.doCalculus(self.j2_test, True)

    def doCalculusJ3(self):
        return self.doCalculus(self.j3_test, True)

    def doCalculusJ4(self):
        return self.doCalculus(self.j4_test, True)

    def doCalculus(self, m_j: json, b_serialize: bool, flag: bool = True) -> json:
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
                self.p = PosteMetier(pid)
                self.o_test = self.p_test.observation(m_j['data'][idx]['current']['dat'])
                if self.o_test.data.duration == 0:
                    self.o_test.data.duration = m_j['data'][idx]['current']['duration']
                self.a_test = self.p_test.aggregations(m_j['data'][idx]['current']['dat'], m_j['data'][idx]['current']['duration'])

                # call the method to update obs, and return delta_val
                all_instr.process_json(self.p_test, m_j, idx, self.o_test, self.a_test, True)

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
