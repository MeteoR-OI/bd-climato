#!/usr/bin/python3

import jinja2, os, json
from datetime import datetime
from shutil import copyfile


WEEWX_ROOT = "/srv/weewx/root"
DEFAULT_WUNDERGROUND_PWD='meteor-p455'

# Load config file from station.json
def load_conf(conf_directory, json_file='station.json'):
    SETUP_FILE = os.path.join(conf_directory, json_file)
    conf = {}
    with open(SETUP_FILE, "r") as read_file:
        conf = json.load(read_file)

    # Add some config vars
    conf['station_id_lowcase'] = conf['station_id'].lower()
    if not conf['Wunderground']['password']:
        conf['Wunderground']['password'] = DEFAULT_WUNDERGROUND_PWD
    conf['weewx_root'] = WEEWX_ROOT

    return conf

# Load template file weewx.conf.tpl
def load_tpl(root_directory, tpl=""):
    if not tpl:
        raise Exception("Pas de template indiqué")
    TPL_PATH = os.path.join(root_directory, 'templates')

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TPL_PATH))
    tpl_weewxconf = environment.get_template(tpl)
    
    return tpl_weewxconf

# Backup file
def backup_file(directory, file_name):
    print("Backing up %s" % file_name)
    now = datetime.now()
    TIMESTAMP = now.strftime('%Y%m%d%H%M%S')

    original_file = os.path.join(directory, file_name)
    backup_file   = os.path.join(directory, "%s.%s" % (file_name, TIMESTAMP))

    if not os.path.isfile(original_file):
        print("%s n'existe pas." % original_file)
        return False

    copyfile(original_file, backup_file)

    return



