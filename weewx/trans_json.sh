#!/bin/bash

# Save json files to json_archive :
mv /srv/weewx/root/public_html/json/*.json /srv/weewx/root/json_archive && echo "save files json ok"
# clear json files older than 1 days
find /srv/weewx/root/json_archive/*.json -mtime +7 -exec rm {} \; && echo "clear files json ok"
