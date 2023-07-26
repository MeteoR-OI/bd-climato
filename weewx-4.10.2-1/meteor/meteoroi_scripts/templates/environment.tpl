#!/bin/bash

WEEWX_USER="{{ weewx_user|default('weewx') }}"
STATION_ID="{{ station_id|default('XXX000') }}"
# La ligne a été ajoutée dans /etc/bash.bashrc 
# STATION_ID_LOWERC=`echo $STATION_ID | tr '[:upper:]' '[:lower:]'`

