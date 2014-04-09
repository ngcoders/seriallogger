#!/bin/sh
python --version
echo
echo "Configuring ip address now"
. /boot/netConfig.dat
echo "Setting your ip address at "$rasp_ip_addr
ifup eth0
ifconfig eth0 $rasp_ip_addr netmask $rasp_net_mask broadcast $rasp_broadcast
route add default gw $rasp_gate_way eth0
cd /home/serialLogger/
python server.py &
python logger.py &
echo


