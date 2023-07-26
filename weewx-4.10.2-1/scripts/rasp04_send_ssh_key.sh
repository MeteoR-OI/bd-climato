#!/bin/bash

#cat /srv/$WEEWX_USER/.ssh/id_rsa.pub | ssh $STATION_ID_LOWERC@obs.meteor-oi.re "cat - >> /srv/data/meteor/stations/$STATION_ID/.ssh/authorized_keys"

STATION_ID_LOWERC=`echo $STATION_ID | tr '[:upper:]' '[:lower:]'`

#echo "Enter password then CTRL+C"


#ssh -tt ${STATION_ID_LOWERC}@obs.meteor-oi.re /bin/bash << EOF
#    hostname -A;
#    ssh xxx000@127.0.0.1;
#EOF

scp /srv/$WEEWX_USER/.ssh/id_rsa.pub $STATION_ID_LOWERC@obs.meteor-oi.re:/srv/stations/$STATION_ID/.ssh/authorized_keys

exit 0
