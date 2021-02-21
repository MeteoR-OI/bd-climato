import unittest
from app.tools.jsonPlus import JsonPlus
import datetime


class TestScript(unittest.TestCase):
    jp = JsonPlus()
    z = jp.json_test()

    def load_json_from_string(self):
        # load a json, with date as a str
        jj = self.jp.loads(self.z)
        # all dates are datetime after loads
        assert str(isinstance(jj['data'][0]['current']['dat'], datetime.datetime))

    def dumps_loads(self):
        jj = self.jp.loads(self.z)
        jj2 = self.jp.loads(self.jp.dumps(jj))
        assert str(self.jp.dumps(jj2) == self.jp.dumps(jj))

    def serialize(self):
        jj = self.jp.loads(self.z)
        self.jp.serialize(jj)
        assert isinstance(jj['data'][0]['current']['dat'], str)

    def deserialize(self):
        jj = self.jp.loads(self.z)
        self.jp.serialize(jj)
        self.jp.deserialize(jj)
        assert isinstance(jj['data'][0]['current']['dat'], datetime)
