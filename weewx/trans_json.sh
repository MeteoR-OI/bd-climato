#!/bin/bash
 
# Save json files to json_archive :
if mv /srv/weewx/root/public_html/json/*.json /srv/weewx/root/json_archive
then
echo "save files json ok"
fi
# clear json files older than 1 days
if find /srv/weewx/root/json_archive/*.json -mtime +1 -exec rm {} \
echo "clear files json ok"
fi
