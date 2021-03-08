# import datetime
from django.test import TestCase
# from django.utils import timezone
from app.classes.integrationTests.typeTemp import type_temp_test


class TypeTempTest(TestCase):
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

    def __init__(self):
        self.tt = type_temp_test()

    def simple_aggregation_hour(self):
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
