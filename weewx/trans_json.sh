#!/bin/bash
 
# Transferer obs.json vers mac Hubert :
rm /srv/weewx/root/public_html/json/obs*.json
chmod 777 /srv/weewx/root/public_html/json/obs*.json && echo "mod lecture/ecriture pour tous"
if rsync -v /srv/weewx/root/public_html/json/obs*.json weewx@machubert.local:/Users/hubertquetelard/Documents/MeteoROI/bd-climato/data/json_auto_load
then
echo "transfert ok"
mv /srv/weewx/root/public_html/json/obs*.json /srv/weewx/root/dev/json && echo "archivage json ok"
else
echo "transfert ko"
fi
