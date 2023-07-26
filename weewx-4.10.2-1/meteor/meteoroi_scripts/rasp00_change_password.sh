#!/bin/bash

apt-get update
apt-get dist-upgrade --yes --auto-remove --show-upgraded

# Change passwords
NEW_PASSWORD="${STATION_ID}-p455"

usermod --password $(openssl passwd -1 $NEW_PASSWORD) pi
usermod --password $(openssl passwd -1 $NEW_PASSWORD) meteor 

