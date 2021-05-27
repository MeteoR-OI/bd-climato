#
#    Copyright (c) 2009-2015 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

"""User extensions module

This module is imported from the main executable, so anything put here will be
executed before anything else happens. This makes it a good place to put user
extensions.
"""

import locale
# This will use the locale specified by the environment variable 'LANG'
# Other options are possible. See:
# http://docs.python.org/2/library/locale.html#locale.setlocale
#locale.setlocale(locale.LC_ALL, '')

# added by
#  QUETELARD
from datetime import datetime
import os
# end added

import weewx.manager
import weecfg

# added by QUETELARD
# when program start, in first get lastUpdate of database
file_name = os.environ['HOME'] + "/root/weewx.conf"
config_dict = weecfg.read_config(file_name)
config_dict = config_dict[1]
db_binding = 'wx_binding'
dbm = weewx.manager.open_manager_with_config(config_dict,db_binding)
last_update_stop = int(dbm._read_metadata('lastUpdate'))
dbm.close
# end added
