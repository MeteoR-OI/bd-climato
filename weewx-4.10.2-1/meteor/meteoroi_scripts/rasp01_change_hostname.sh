#!/bin/bash

CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
echo $STATION_ID > /etc/hostname
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$STATION_ID/g" /etc/hosts


