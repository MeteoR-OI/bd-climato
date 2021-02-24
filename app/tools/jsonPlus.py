
import json
import dateutil.parser
import datetime


class JsonPlus():
    """ super class adding date serialization/deserialization aupport """

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
                            "dat" : "2021-02-11T13:09:30+00:00",
                            "duration" : 300,
                            "out_temp" : 29.5,
                            "out_temp_max": 30.1,
                            "out_temp_max_time": "2021-02-11T13:09:32+00:00"
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
        """ encode str fields into datetime for our well known keys """
        if isinstance(j, dict) or isinstance(j, JsonPlus):
            # print("serialize(" + json.dumps(j))
            for k, v in j.items():
                # print("Decode: " + k + ":" + str(j[k]) + ", type: " + str(type(j[k])))
                if 'dat' == k:
                    j[k] = dateutil.parser.parse(str(j[k]))
                    # print("found dat, new type : " + str(type(j[k])))
                if 'last_dat_rec' == k:
                    j[k] = dateutil.parser.parse(str(j[k]))
                    # print("found last_dat_rec, new type : " + str(type(j[k])))
                if k.endswith('_time'):
                    j[k] = dateutil.parser.parse(str(j[k]))
                    # print("found xxx_time, new type : " + str(type(j[k])))
                if isinstance(j[k], dict) or isinstance(j[k], JsonPlus):
                    # print("** going down... **")
                    self.deserialize(j[k])
                if isinstance(j[k], list):
                    for akey in j[k]:
                        if isinstance(akey, dict) or isinstance(akey, JsonPlus):
                            # print("   ** going down... **")
                            self.deserialize(akey)
                # print("----- loop -----")
        return j

    def serialize(self, j: dict):
        """ encode datetime into str format """
        try:
            if isinstance(j, dict) or isinstance(j, JsonPlus):
                # print("serialize(" + json.dumps(j))
                for k, v in j.items():
                    # print("serialize: " + k + ", type: " + str(type(j[k])))
                    if isinstance(v, (datetime.date, datetime.datetime)):
                        j[k] = v.isoformat()
                        # print("   serialize " + k + ", new type: " + str(type(j[k])))
                    if isinstance(j[k], dict) or isinstance(j[k], JsonPlus):
                        # print("   ** going down... **")
                        self.serialize(j[k])
                    if isinstance(j[k], list):
                        for akey in j[k]:
                            if isinstance(akey, dict) or isinstance(akey, JsonPlus):
                                # print("   ** going down... **")
                                self.serialize(akey)
                    # print("----- loop -----")
            return j
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,


# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime to str """
    # Override the default method

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
