#!/bin/bash
 
STATIONID=$STATION_ID 

mysqldump -u dbbackup weewx_$STATIONID > /srv/weewx/backups/weewx_${STATIONID}.sql
 
# Sauvegarder : 
# - weewx.conf
# - skin.conf
# - public_html
cp /srv/weewx/root/weewx.conf /srv/weewx/backups/weewx.conf && echo "weewx.conf saved!"
cp /srv/weewx/root/skins/Bootstrap/skin.conf /srv/weewx/backups/bootstrap_skin.conf && echo "skin.conf saved!"
tar czvf /srv/weewx/backups/public_html.tar.gz /srv/weewx/root/public_html && echo "public_html saved!"

