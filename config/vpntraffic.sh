#!/bin/sh

source secrets.env

AGE=$(( ($(date +%s) - $(stat /config/vpntraffic.txt  -c %Y)) / 60 ))

if [[ $AGE -gt 5 ]]; then
  ssh -o ConnectTimeout=20 -i /config/ssh/id_rsa -o StrictHostKeyChecking=no $OPNSENSE "wg show" > /config/vpntraffic.txt
  sleep 0.5
fi

python vpntraffic.py $1
