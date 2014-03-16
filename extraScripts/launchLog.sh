#!/bin/sh
python --version
echo "Bringing up GPS Serial"
modprobe usbserial vendor=0x09d7 product=0x0100
echo "Configuring ip address now"
. /boot/netConfig.dat
echo "Setting your ip address at "$rasp_ip_addr
ifconfig eth0 $rasp_ip_addr netmask $rasp_net_mask
cd /home/serialLogger/
python server.py &
python logger.py &
echo


