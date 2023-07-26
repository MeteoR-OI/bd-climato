#!/bin/bash

echo "CREATE DATABASE IF NOT EXISTS weewx_${STATION_ID};
CREATE USER IF NOT EXISTS 'weewx'@'localhost';
SET PASSWORD FOR 'weewx'@'localhost' = PASSWORD('J_Gs_irG_W');
SET PASSWORD FOR 'meteor'@'localhost' = PASSWORD('${STATION_ID}-p455');
GRANT ALL PRIVILEGES ON weewx_${STATION_ID}.* TO 'weewx'@'localhost';
FLUSH PRIVILEGES;" | mysql -u root -p6DI+mrlnTW


