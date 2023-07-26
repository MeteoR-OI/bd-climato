#!/usr/bin/python3

import jinja2, os, json
from datetime import datetime
from shutil import copyfile
from utils import utils

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
ETC = "/etc"

# Load config file from station.json
conf = utils.load_conf(SCRIPT_PATH, 'station.json')

if conf == {}:
    exit()


CFG_FILE_NAMES = ["environment", "bash.bashrc"]
for cfg_file_name in CFG_FILE_NAMES:
    # Load template files
    tpl = utils.load_tpl(SCRIPT_PATH, "%s.tpl" % cfg_file_name)

    # Backup file
    utils.backup_file(ETC, cfg_file_name)

    # Render template
    print("Rendering %s" % cfg_file_name)
    output_cfg = tpl.render(conf)

    test_file = os.path.join(SCRIPT_PATH, '%s.test' % cfg_file_name)
    dest_file = os.path.join(ETC, cfg_file_name)
    with open(dest_file, "w") as rendered_file:
    #with open(test_file, "w") as rendered_file:
        rendered_file.write(output_cfg)

exit()



