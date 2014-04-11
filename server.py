from bottle import *
import sys
import os
import signal
import functions 
import datetime
import re
import platform
import socket
import commands
import ConfigParser
import threading, time
from time import sleep

class serverActivity(threading.Thread):
        isProcessor = 0
	_mgpioPinNumber = 0
        def __init__(self , gpioNumber):
		threading.Thread.__init__(self)
                self.isProcessor = functions.isProcessorType()                
                #_mStateLed_onGpio =  gpioState
		self._mgpioPinNumber = gpioNumber
                
        def run(self):
		try:
			if ( self.isProcessor != 0 ):
                        	# rpi Code executes/ goes here
                        	import RPi.GPIO as GPIO_RPI                                
				GPIO_RPI.setmode( GPIO_RPI.BOARD )
				GPIO_RPI.setwarnings(0)
                        	GPIO_RPI.setup(int(self._mgpioPinNumber), GPIO_RPI.OUT )
                        	GPIO_RPI.output(int(self._mgpioPinNumber), 0)# on LED.                                                                        
				#print "Led configured"
                        	time.sleep( 5 )
                        	GPIO_RPI.output(int(self._mgpioPinNumber), 1)# off the LED
                	else:                        
                        	print "This is not an ARM machine"
                        	time.sleep(5)
		except:
			print "Something went wrong at this point, inside serverActivity Module"
			print sys.exc_info()
                                

class allTimeSystemDevice(threading.Thread):
        _machineStateLED_onGpio = 0
        def __init__(self, isgpio, isOnState):
                threading.Thread.__init__(self)
                self.isState = isOnState - 1
		self._machineStateLED_onGpio = isgpio
                
        def run(self):

                try:
                        __IsArmProcessor__ = functions.isProcessorType()                        
                        # on the led state of Led 1
                        if (__IsArmProcessor__ != 0):
                                
                                import RPi.GPIO as GPIO_RPI    
				GPIO_RPI.setwarnings( 0 )                            
				GPIO_RPI.setmode( GPIO_RPI.BOARD )
                                GPIO_RPI.setup(int(self._machineStateLED_onGpio), GPIO_RPI.OUT )
				#print self.isState, self._machineStateLED_onGpio
                                GPIO_RPI.output(int(self._machineStateLED_onGpio), int(self.isState))
                                # isState is 0, false, low.change this data according to led config. high or low.
                                
                              # alwasy on till this thread is on
                        else:
                                print "	     This is always on as the server is On."
				print "      Detected That this is not an arm machine"

                except:
                        print "Something goes wrong"
			print sys.exc_info()
                        
#take server gpio data setting from setting config file
configs = ConfigParser.ConfigParser()
configs.read("settings.cfg")
server_gpio = str(configs.get("generic_config","server_gpio"))
thisDevice = allTimeSystemDevice(server_gpio,1)# on the server indication led, same for logger.
thisDevice.start()
server = Bottle()
#print "Starting Logger Now..."
#os.system("python /home/serialLogger/logger.py")


@server.route('/media/<filepath:path>')
def server_static(filepath):
	curDir = commands.getoutput('pwd')
	curDir += '/media/'
	#print curDir
        return static_file(filepath, root= curDir)


@server.route('/')
def default() :
	
	# wait for a while here. To avoid errors.
	time.sleep(1)	
        #print functions.runThisCommand('pwd')print current working directory
	try:
		files = os.listdir('logs/')
		hostName = kernelVersionValue = ipAddressEth = netMaskAddr = nSizeofCurDisk ='na'
		nSizeUsed = nSizeNotUsed = 'na'
		#declaring default values...
	except:
		print ' logs/ , folder not found or not allowed to read and write. Please check its existence.'
		print sys.exc_info()
	try:
		CurTime = ''
		upSysTime = ''
		CurTime = functions.getRequiredFieldData('curtime')
	        upSysTime = functions.getRequiredFieldData( 'upTime' )
	        CurTime = ': %s Hrs' %CurTime    
	        upSysTime = ": %s Hrs"%upSysTime
		
	except:
		print ' Something went wrong, getting current time/getting uptime. Please check parsing.'
		print sys.exc_info()

        
	
	try:
		hostName = 'na'
		kernelVersionValue = 'na'
		ipAddressEth = 'na'
		netMaskAddr = 'na'
		nSizeofCurDisk = 'na'
		nSizeUsed = 'na'
		nSizeNotUsed = 'na'
		
	        hostName = functions.getRequiredFieldData( 'host' )        
	        kernelVersionValue =  functions.getRequiredFieldData( 'kernel')        
	        ipAddressEth0 = functions.getRequiredFieldData( 'ipaddr' )
	        netMaskAddr = functions.getRequiredFieldData( 'netMask' )        
	        nSizeofCurDisk = functions.getRequiredFieldData( 'totalSpace' )
        	nSizeUsed = functions.getRequiredFieldData( 'usedSpace' )
        	nSizeNotUsed = functions.getRequiredFieldData( 'freeSpace' )
		nSizeofCurDisk+="B"
        	nSizeUsed+="B"
        	nSizeNotUsed+="B"
	except:
		print ' Please check for parsing.host/kernel/ipaddr/netmask/totalspace parsing issue.'
		print sys.exc_info()

        
        
        return template('default',files=files, upTime=upSysTime, nowTime= CurTime, kerVer=kernelVersionValue, hostNameIs = hostName , ipAddrEth0 = ipAddressEth0, totalNetSpace = nSizeofCurDisk, notUsed = nSizeNotUsed, usedSpace = nSizeUsed , netMaskField = netMaskAddr )
        
        
@server.route('/download/<filename>')
def download(filename) :
        # IPC to write

        # code for rPi goes here, to hold led for a while
	
	try:    
		# call to write log and then allow to download.
		pids = str(commands.getoutput("ps -aux | grep logger"))
		proc_data = re.search(r"root\s+(\w+)", pids)
		#for this condition, logger must be running, else it will pick wring pid.
		os.kill(int(proc_data.group(1)), signal.SIGUSR1)
		#time.sleep( 10  )# wait for few seonds say for 10, and let the logger do its work. Logger will start logging at pont when it gets SIGUSR1 signal.
		conFigs = ConfigParser.ConfigParser()
		conFigs.read("settings.cfg")
		dwn_gpioLed = str(conFigs.get("generic_config","dwn_gpio"))
	       	serverDAct = serverActivity(dwn_gpioLed)
       		serverDAct.start()
	except:
		print "Something went wrong at download procedure here, please check parsing, or settings.cfg file not found "
		print sys.exc_info()
        
        return static_file(filename, root= 'logs/', download=filename)

@server.route('/truncate/<filename>')
def truncate(filename) :

	# Truncate file
	try:
		tfile = open('logs/'+filename,"wb")
		tfile.write("")
		tfile.close()
	except:
		print ' may be, file not found, or opened already by some other app. Please check its existence.'
		print sys.exc_info()

	redirect('/')


@server.route('/delete/<filename>')
def truncate(filename) :
	# Truncate file
	try:
		os.remove('logs/'+filename)
	except:
		print 'casued error due to, may be file opened already by some other application, please check its existence'
		print sys.exc_info()

	redirect('/')	

@server.route('/help') 
def help() :
        return template('help')

@server.route('/reboot')
def reboot():	
	os.system('reboot')
	return template('reboot')
	
@server.route('/config')  
def config() :
	try:
        	config = ConfigParser.ConfigParser()
        	config.read('settings.cfg')
	except:
		print ' error caused due to: file not found settings.cfg, please check its existence.'
		print sys.exc_info()

	return template('config',config=config)

@server.route('/config', method="POST") 
def save_config() :
        # settings to save, code goes here
        #redirect('/') to redirect to main page
        # below code can be optimized by looping, although three ports are fixed and not going to change, hence kpt the code static
	try:
		configBefore = ConfigParser.ConfigParser()
		configBefore.read("settings.cfg")
	except:
		print sys.exc_info()
	try:
        	configParsingInst = ConfigParser.ConfigParser()
	        configFile = open("settings.cfg",'w')
	except:
		print ' error caused due to: file not found settings.cfg, please check its existence.'
		print sys.exc_info()

	try:
		for nCount, secNm in enumerate(['serial','gps1', 'gps2']):
		        configParsingInst.add_section(secNm)
		        serialDataList = request.forms.getlist(secNm)
		        configParsingInst.set(secNm, 'Device',serialDataList[0] )        
		        configParsingInst.set(secNm, 'baudrate', serialDataList[1])
			configParsingInst.set(secNm, 'gpio', serialDataList[2])

		configParsingInst.write(configFile)
		configFile.close()
	except:
		print 'something went wrong in parsing section in config file, read write error.'
		print sys.exc_info()
	
	try:
		#now append the rest of the changes again back in to file
		configAfter = ConfigParser.ConfigParser()
		configAfterFile = open("settings.cfg","a")
	except:
		print ' error caused due to: file not found settings.cfg, please check its existence.'
		print sys.exc_info()

	try:
		secNameAfter = configBefore.sections()[-1]
		configAfter.add_section(secNameAfter)
		configAfter.set(secNameAfter, "server_gpio", "12")# hard coded for server. gpio.
		configAfter.set(secNameAfter,"dwn_gpio", "16")# for download blink. gpio.

		configAfter.write(configAfterFile)
		configAfterFile.close()

		#end of writing config settings file with all information
	except:
		print 'read write error with config file, please check for its existence.'
		print sys.exc_info()
	try:
		procDataFrom = str(commands.getoutput("ps -aux | grep logger"))
		proc_data = re.search(r"root\s+(\w+)", procDataFrom)
		os.system("kill -9 " + str(proc_data.group(1)))	
		os.system("python logger.py & ")
	except:
		print ' Not able to relaunch the logger , please check for its instance running or not running.'
		print sys.exc_info()

	redirect('/')

''' simple user login for future '''

@server.route('/login')
def login():
        return template('login')

@server.route('/login', method='POST')
def do_login():
        return template('login')        

BaseTemplate.defaults['route'] = request

run(server,reloader=True,host="0.0.0.0",port='8080',debug = True)

