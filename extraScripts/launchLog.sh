#!/bin/sh
python --version
echo
echo "Configuring ip address now"
. /boot/netConfig.dat
echo "Setting your ip address at "$rasp_ip_addr
ifconfig eth0 $rasp_ip_addr netmask $rasp_net_mask
cd /home/serialLogger/
python server.py &
python logger.py &
echo


