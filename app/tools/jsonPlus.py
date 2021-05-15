from app.tools.dateTools import date_to_str, str_to_date
import datetime
import json
import sys


class JsonPlus():
    """ super class adding date serialization/deserialization support """

    def dumps(self, j: json) -> str:
        """
        dumps
            return a string from a json with datetime values

        Parameter:
            json with date values
        """
        try:
            ret = json.dumps(j, cls=DateTimeEncoder)
            self.deserialize(j)
            return ret
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e

    # custom Decoder
    def loads(self, json_str: str) -> json:
        """
        loads
            load json from a string, and deserialize datetime fields

        Parameter:
            json data in a string field
        """
        try:
            return json.loads(json_str, object_hook=self.customDecoder)
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e

    def customDecoder(self, jsonDict: dict) -> str:
        """
        customDecoder
            Hook to parse str to datetime
        """
        try:
            self.deserialize(jsonDict)
            return jsonDict
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e

    def deserialize(self, j: dict):
        """
        deserialize
            deserialize date in str format to datetime

        Parameter
            json field with stringified date
        Note
            only keys with stop_dat, start_dat, end with '_time' will be deserialized
        """
        try:
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
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e

    def serialize(self, j: dict):
        """
        serialize
            encode datetime values into str format

        Parameter:
            json data to serialize
        """
        try:
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
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e


# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    """
    DateTimeEncoder
        Class to encode datetime to str
    """
    # Override the default method
    def default(self, obj):
        try:
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return date_to_str(obj)
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            raise e
