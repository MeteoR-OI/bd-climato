#!/bin/bash

cd /home/meteor/meteoroi_scripts/tmp/root/tmp_vpn
sudo mv ${STATION_ID}/* /etc/openvpn/
cd /home/meteor/meteoroi_scripts
rm -rf tmp

