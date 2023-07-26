#!/bin/bash

echo "Stopping weewx"
sudo systemctl stop weewx

echo "Dropping weewx database"
echo "DROP DATABASE IF EXISTS weewx_XXX000;
DROP DATABASE IF EXISTS  weewx_${STATION_ID};
CREATE DATABASE weewx_${STATION_ID};
FLUSH PRIVILEGES;" | sudo mysql -u root -p6DI+mrlnTW

echo "Removing weewx generated files"
sudo rm -rf /srv/weewx/root/public_html/*

echo "Restart Weewx"
sudo systemctl restart weewx

exit;
