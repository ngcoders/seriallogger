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
	Four fields:
		1. ip address.
		2. netmask address.
		3. gateway address.
		4. broadcast address.
	These are required, as dhcp is disabled and we have to explicitly mention for doing static settings.
	In this file you can set up your logger ip address and netmask.

+ Installing this source
	- Put this inside /home folder, mind the lettter case. This, it will appear /home/serialLogger

+ Disable dhcp in raspberry pi, so the static configuration will take over.
	- go to /etc/network/interface file.
	- using any file editor, under root, 
	- change the "iface eth0 inet dhcp" to "iface eth0 inet static"
	- save.
	- Rest of the configuration will be done by other scripts on the basis of netConfig.dat content.

+ If required,
	- Set up bits of file for execution
	- In command prompt,
	- log in as root
		- > su
		- password: xxxx
		- >cd /etc/init.d/
		- >chmod 775 launchLog.sh
		- >update-rc.d launchLog.sh defaults
		- >reboot

============


