#!/bin/bash

cd /home/meteor/meteoroi_scripts
mkdir tmp && cd tmp
wget http://obs.meteor-oi.re/files/VPN_${STATION_ID}.tar.gz
tar xzvf VPN_${STATION_ID}.tar.gz
cd root/tmp_vpn/${STATION_ID}
sudo openvpn --config MeteoR_OI.conf
cd /home/meteor/meteoroi_scripts

