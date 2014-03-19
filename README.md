SerialLogger
============

+ Based on
	- Raspberry Pi

+ Channels
	- Three channels or say ports

+ Feature
	- Customize device port, gpio and baud rate
	- Download log files
	- Know current status of the logger

+ Configuration file
	- launchLog.sh
	Put this file inside /etc/init.d folder. As this file will launch the logger program at startup
	- netConfig.dat - Put this file inside /boot/ folder.
	In this file you can set up your logger ip address and netmask.

+ Installing this source
	- Put this inside /home folder, mind the lettter case. This, it will appear /home/serialLogger

+ If required,
	- Set up bits of file for execution
	-In command prompt,
	-log in as root
		- > su
		- password: xxxx
		- >cd /etc/init.d/
		- >chmod 775 launchLog.sh
		- >update-rc.d launchLog.sh defaults
		- >reboot

============


