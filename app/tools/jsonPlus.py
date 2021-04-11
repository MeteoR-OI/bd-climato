import json
import datetime
from app.tools.dateTools import date_to_str, str_to_date


class JsonPlus():
    """ super class adding date serialization/deserialization support """
    def json_test(self) -> str:
        """ json sample for future testing """
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
                            "dat" : "2021-02-11T13:09:30",
                            "duration" : 5,
                            "out_temp" : 29.5,
                            "out_temp_max": 30.1,
                            "out_temp_max_time": "2021-02-11T13:09:32"
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
                            "dat" : "2021-02-11T13:09:40",
                            "duration" : 5,
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
        return json_string

    def dumps(self, j: json) -> str:
        """ serialize json with date values """
        ret = json.dumps(j, cls=DateTimeEncoder)
        self.deserialize(j)
        return ret

    # custom Decoder
    def loads(self, json_str: str) -> json:
        """ load json from a string, and deserialize datetime fields """
        return json.loads(json_str, object_hook=self.customDecoder)

    def customDecoder(self, jsonDict: dict) -> str:
        """ Hook to parse str to datetime """
        self.deserialize(jsonDict)
        return jsonDict

    def deserialize(self, j: dict):
        if isinstance(j, str):
            j = JsonPlus().loads(j)
        """ encode str fields into datetime for our well known keys """
        if isinstance(j, dict) or isinstance(j, JsonPlus):
            for k, v in j.items():
                if 'start_dat' == k or 'stop_dat' == k or 'dat' == k or k.endswith('_time'):
                    j[k] = str_to_date(j[k])
                if isinstance(j[k], list):
                    for akey in j[k]:
                        if isinstance(akey, dict) or isinstance(akey, JsonPlus):
                            self.deserialize(akey)
                if isinstance(j[k], dict):
                    self.deserialize(j[k])
        return j

    def serialize(self, j: dict):
        """ encode datetime into str format """
        if isinstance(j, dict) or isinstance(j, JsonPlus):
            for k, v in j.items():
                if isinstance(v, (datetime.date, datetime.datetime)):
                    tmp_date = date_to_str(v)
                    if tmp_date.find("+") > -1:
                        tmp_date = tmp_date[:tmp_date.find("+")]
                    j[k] = tmp_date
                if isinstance(j[k], dict) or isinstance(j[k], JsonPlus):
                    self.serialize(j[k])
                if isinstance(j[k], list):
                    for akey in j[k]:
                        if isinstance(akey, dict) or isinstance(akey, JsonPlus):
                            self.serialize(akey)
        return j


# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime to str """
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return date_to_str(obj)
