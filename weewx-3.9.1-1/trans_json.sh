#!/bin/bash

# Save json files older than 1 day to json_archive :
find /srv/weewx/root/public_html/json/obs*.json -mtime +1 -exec mv {} /srv/weewx/root/json_archive \; && echo "save obs files json ok"
find /srv/weewx/root/public_html/json/arch.json -mtime +1 -exec mv {} /srv/weewx/root/json_archive \; && echo "save arch files json ok"
# clear json files in json_archive older than 7 days
find /srv/weewx/root/json_archive/*.json -mtime +7 -exec rm {} \; && echo "clear files json ok"
