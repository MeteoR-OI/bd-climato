#
#    Copyright (c) 2009-2014 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
#    $Id: xsearch.py 2766 2014-12-02 02:45:36Z tkeffer $
#

"""Example of how to extend the search list used by the Cheetah generator.

This search list extension offers two extra tags:

    'alltime':   All time statistics.
                 For example, "what is the all time high temperature?"

    'seven_day': Statistics for the last seven days.
                 That is, since midnight seven days ago.

To use it, modify the option search_list in your skin.conf configuration file,
adding the name of this extension. For this example, the name of the extension
is examples.xsearch.MyXSearch. So, when you're done, it will look something
like this:

[CheetahGenerator]
    search_list_extensions = examples.xsearch.MyXSearch

Note that if your file skin.conf is from an older version of Weewx, this
section may be named [FileGenerator]. It will work just fine.

You can then use tags such as $alltime.outTemp.max for the all-time max
temperature, or $seven_day.rain.sum for the total rainfall in the last
seven days.
"""
import datetime
import time

from weewx.cheetahgenerator import SearchList
from weewx.tags import TimespanBinder
from weeutil.weeutil import TimeSpan

class TimePeriod(SearchList):
    """My search list extension"""

    def __init__(self, generator):
        SearchList.__init__(self, generator)
    
    def get_extension_list(self, timespan, db_lookup):
        """Returns a search list extension with two additions.
        
        Parameters:
          timespan: An instance of weeutil.weeutil.TimeSpan. This will
                    hold the start and stop times of the domain of 
                    valid times.

          db_lookup: This is a function that, given a data binding
                     as its only parameter, will return a database manager
                     object.
        """
        dt_last = datetime.datetime.fromtimestamp(timespan.stop)

        # Direct :
        last_hour_dt = dt_last - datetime.timedelta(hours=1)
        last_hour_ts = time.mktime(last_hour_dt.timetuple())
        last_hour_stats = TimespanBinder(TimeSpan(last_hour_ts, timespan.stop),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)


        three_hours_dt = dt_last - datetime.timedelta(hours=3)
        three_hours_ts = time.mktime(three_hours_dt.timetuple())
        three_hours_stats = TimespanBinder(TimeSpan(three_hours_ts, timespan.stop),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        six_hours_dt = dt_last - datetime.timedelta(hours=6)
        six_hours_ts = time.mktime(six_hours_dt.timetuple())
        six_hours_stats = TimespanBinder(TimeSpan(six_hours_ts, timespan.stop),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        twelve_hours_dt = dt_last - datetime.timedelta(hours=12)
        twelve_hours_ts = time.mktime(twelve_hours_dt.timetuple())
        twelve_hours_stats = TimespanBinder(TimeSpan(twelve_hours_ts, timespan.stop),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        twentyfor_hours_dt = dt_last - datetime.timedelta(hours=24)
        twentyfor_hours_ts = time.mktime(twentyfor_hours_dt.timetuple())
        twentyfor_hours_stats = TimespanBinder(TimeSpan(twentyfor_hours_ts, timespan.stop),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        search_list_extension = {'last_hour'       : last_hour_stats,
                                 'three_hours'     : three_hours_stats,
                                 'six_hours'       : six_hours_stats,
                                 'twelve_hours'    : twelve_hours_stats,
                                 'twentyfour_hours': twentyfor_hours_stats,}

        # Heure fixe
        dt_last_rounded = dt_last.replace(minute=0, second=0, microsecond=0)
        dt_last_rounded_ts = time.mktime(dt_last_rounded.timetuple())

        last_hour_fixed_dt = dt_last_rounded - datetime.timedelta(hours=1)
        last_hour_fixed_ts = time.mktime(last_hour_fixed_dt.timetuple())
        last_hour_fixed_stats = TimespanBinder(TimeSpan(last_hour_fixed_ts, dt_last_rounded_ts),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        three_hours_fixed_dt = dt_last_rounded - datetime.timedelta(hours=3)
        three_hours_fixed_ts = time.mktime(three_hours_fixed_dt.timetuple())
        three_hours_fixed_stats = TimespanBinder(TimeSpan(three_hours_fixed_ts, dt_last_rounded_ts),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        six_hours_fixed_dt = dt_last_rounded - datetime.timedelta(hours=6)
        six_hours_fixed_ts = time.mktime(six_hours_fixed_dt.timetuple())
        six_hours_fixed_stats = TimespanBinder(TimeSpan(six_hours_fixed_ts, dt_last_rounded_ts),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        twelve_hours_fixed_dt = dt_last_rounded - datetime.timedelta(hours=12)
        twelve_hours_fixed_ts = time.mktime(twelve_hours_fixed_dt.timetuple())
        twelve_hours_fixed_stats = TimespanBinder(TimeSpan(twelve_hours_fixed_ts, dt_last_rounded_ts),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        twentyfour_hours_fixed_dt = dt_last_rounded - datetime.timedelta(hours=24)
        twentyfour_hours_fixed_ts = time.mktime(twentyfour_hours_fixed_dt.timetuple())
        twentyfour_hours_fixed_stats = TimespanBinder(TimeSpan(twentyfour_hours_fixed_ts, dt_last_rounded_ts),
                                           db_lookup,
                                           formatter=self.generator.formatter,
                                           converter=self.generator.converter)

        search_list_extension.update({
             'fixed_last_hour'       : last_hour_fixed_stats,
             'fixed_three_hours'     : three_hours_fixed_stats,
             'fixed_six_hours'       : six_hours_fixed_stats,
             'fixed_twelve_hours'    : twelve_hours_fixed_stats,
             'fixed_twentyfour_hours': twentyfour_hours_fixed_stats,
        })

        return [search_list_extension]
