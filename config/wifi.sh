#!/bin/bash

source secrets.env

aps=( $APS )

if [[ $1 == "gueststatus" ]]; then
status=$(ssh -o ConnectTimeout=20 -i /config/ssh/id_rsa -o StrictHostKeyChecking=no ${aps[1]} "uci get wireless.wifinet4.disabled")
echo $status
elif [[ $1 == "gueston" ]]; then
for i in "${aps[@]}"
do
	ssh -o ConnectTimeout=20 -i /config/ssh/id_rsa -o StrictHostKeyChecking=no $i "/root/guest.sh on"
done
elif [[ $1 == "guestoff" ]]; then
for i in "${aps[@]}"
do
	ssh -o ConnectTimeout=20 -i /config/ssh/id_rsa -o StrictHostKeyChecking=no $i "/root/guest.sh off"
done
elif [[ $1 == "restart" ]]; then
for i in "${aps[@]}"
do
	ssh -o ConnectTimeout=20 -i /config/ssh/id_rsa -o StrictHostKeyChecking=no $i "reboot"
    sleep 4
done
fi
