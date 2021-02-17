
import json
import dateutil.parser
import datetime


class jsonPlus():
    """ super class adding date serialization/deserialization aupport """

    def json_test(self) -> str:
        """ json sample for future testing """
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
        return json_string

    def dumps(self, j: json) -> str:
        """ serialize json with date values """
        return json.dumps(j, cls=DateTimeEncoder)

    # custom Decoder
    def loads(self, json_str: str) -> json:
        """ deserialize key dat and last_rec_dat """
        return json.loads(json_str, object_hook=self.customDecoder)

    def customDecoder(self, jsonDict: dict) -> str:
        """ Hook to parse str to datetime """
        self.rec_json(jsonDict)
        return jsonDict

    def rec_json(self, j: dict):
        """ look recursively in json to find our datetime keys """
        if isinstance(j, dict):
            # print("rec_json(" + json.dumps(j))
            for k, v in j.items():
                # print("Decode: " + k + ":" + str(j[k]) + ", type: " + str(type(j[k])))
                if 'dat' == k:
                    # print('  found dat..')
                    j[k] = dateutil.parser.parse(str(j[k]))
                if 'last_dat_rec' == k:
                    # print('  found last_dat_rec..')
                    j[k] = dateutil.parser.parse(str(j[k]))
                if k.find('_time') > -1:
                    # print('  found end with _time')
                    j[k] = dateutil.parser.parse(str(j[k]))
                if isinstance(j[k], dict):
                    # print("** going down... **")
                    self.rec_json(j[k])
                # print("----- loop -----")


# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime to str """
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
