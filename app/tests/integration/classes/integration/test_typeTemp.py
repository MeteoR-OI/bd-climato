from django.test import TestCase
from app.classes.integrationTests.typeTemp import TypeTempTest


class TypeTempMyTest(TestCase):
    # prefix for json tests
    my_json = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data": []
        }
        """

    def __init__(self, param1):
        self.tt = TypeTempTest()

    def test_simple_aggregation_hour(self, param1):
        """
            Test that measure for rounded hours are agregated in agg_h previous hour
        """
        simple_aggh_json = """
            [
                {"current" : {"dat" : "2021-02-11T13:00:00+00:00", "duration" : 5, "out_temp" : 20}},
            ]
        """
        self.my_json['data'] = simple_aggh_json
        # self.tt.delete_obs_agg()
        resp = self.tt.doCalculus(self.my_json, True)
        self.assertEqual(resp[1]['info'], 'idx=0 - cut and paste this data into https://codebeautify.org/jsonviewer')
