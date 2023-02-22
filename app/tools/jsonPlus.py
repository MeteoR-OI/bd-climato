from app.tools.dateTools import date_to_str, str_to_date
import datetime
import json


class JsonPlus():
    """ super class adding date serialization/deserialization support """

    def dumps(self, j: json) -> str:
        """
        dumps
            return a string from a json with datetime values

        Parameter:
            json with date values
        """
        ret = json.dumps(j, cls=DateTimeEncoder)
        self.deserialize(j)
        return ret

    # custom Decoder
    def loads(self, json_str: str) -> json:
        """
        loads
            load json from a string, and deserialize datetime fields

        Parameter:
            json data in a string field
        """
        if (len(json_str) == 0):
            return {}
        return json.loads(json_str, object_hook=self.customDecoder)

    def customDecoder(self, jsonDict: dict) -> str:
        """
        customDecoder
            Hook to parse str to datetime
        """
        self.deserialize(jsonDict)
        return jsonDict

    def deserialize(self, j: dict):
        """
        deserialize
            deserialize date in str format to datetime

        Parameter
            json field with stringified date
        Note
            only keys with stop_dat, start_dat, end with '_time' will be deserialized
        """
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
        """
        serialize
            encode datetime values into str format

        Parameter:
            json data to serialize
        """
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
    """
    DateTimeEncoder
        Class to encode datetime to str
    """
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return date_to_str(obj)
