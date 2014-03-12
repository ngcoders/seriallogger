from bottle import *
import sys
import os
import functions 
import datetime
import re
import platform
import socket
import commands
import ConfigParser
import threading, time

class serverActivity(threading.Thread):
        isProcessor = 0
        _mStateLed_onGpio = 1
        nCounterforLed = 0
        nCounter = 0
	m_gpioPinNumber = 0
        def __init(self , gpioNumber, gpioState):
                self.isProcessor = functions.isProcessorType()                
                _mStateLed_onGpio =  gpioState
		_mgpioPinNumber = gpioNumber
                
        def run(self):           
                if ( self.isProcessor != 0 ):
                        # rpi Code executes/ goes here
                        import RPi.GPIO as GPIO_RPI                                
			#GPIO_RPI.setmode( GPIO_RPI.BOARD )
                        GPIO_RPI.setup(self._mgpioPinNumber, GPIO_RPI.OUT )
                        GPIO_RPI.output(self._mgpioPinNumber, 0)# on LED.                                                                        
                        time.sleep( 10 )
                        GPIO_RPI.output(self._mgpioPinNumber, 1)# off the LED
                else:                        
                        print "this is printing"
                        time.sleep(5)
                        print "This ends here"
                                

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
                                GPIO_RPI.setup(self._machineStateLED_onGpio, GPIO_RPI.OUT )
				#print self.isState, self._machineStateLED_onGpio
                                GPIO_RPI.output(self._machineStateLED_onGpio, self.isState)
                                # isState is 1, true, High.change thsi data according to led config. high or low.
                                
                              # alwasy on till this thread is on
                        else:
                                print "This is always on as the server is On."

                except:
                        print "Something goes wrong"
			print sys.exc_info()
                        

thisDevice = allTimeSystemDevice(12,1)
thisDevice.start()

server = Bottle()
#print "Starting Logger Now..."
#os.system("python /home/serialLogger/logger.py")


@server.route('/media/<filepath:path>')
def server_static(filepath):
	curDir = commands.getoutput('pwd')
	curDir += '/media/'
	print curDir
        return static_file(filepath, root= curDir)


@server.route('/')
def default() :
	
        #files = os.listdir('dump/')
	print functions.runThisCommand('pwd')
	files = os.listdir('dump/')
      
        CurTime = functions.getRequiredFieldData('curtime')
        upSysTime = functions.getRequiredFieldData( 'upTime' )
        CurTime = ': %s Hrs' %CurTime    
        upSysTime = ": %s"%upSysTime

        if( re.search('min', upSysTime) == None ):
                upSysTime+= ' Hrs'

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
        
        return template('default',files=files, upTime=upSysTime, nowTime= CurTime, kerVer=kernelVersionValue, hostNameIs = hostName , ipAddrEth0 = ipAddressEth0, totalNetSpace = nSizeofCurDisk, notUsed = nSizeNotUsed, usedSpace = nSizeUsed , netMaskField = netMaskAddr )
        
        
@server.route('/download/<filename>')
def download(filename) :
        # IPC to write

        # code for rPi goes here, to hold led for a while
        
        serverDAct = serverActivity(16, 1)
        serverDAct.start()
        
        return static_file(filename, root= 'dump/', download=filename)

@server.route('/truncate/<filename>')
def truncate(filename) :

	# Truncate file
	tfile = open('logs/'+filename,"wb")
	tfile.write("")
	tfile.close()
	redirect('/')


@server.route('/delete/<filename>')
def truncate(filename) :
	# Truncate file
	os.remove('/logs/'+filename)
	redirect('/')	

@server.route('/help') 
def help() :
        return template('help')

@server.route('/reboot')
def reboot():
	os.system('reboot')

@server.route('/config')  
def config() :

        config = ConfigParser.ConfigParser()
        config.read('settings.cfg')
	return template('config',config=config)

@server.route('/config', method="POST") 
def save_config() :
        # settings to save, code goes here
        #redirect('/') to redirect to main page
        # below code can be optimized by looping, although three ports are fixed and not going to change, hence kpt the code static

        configParsingInst = ConfigParser.ConfigParser()
        configFile = open("settings.cfg",'w')

        for nCount, secNm in enumerate(['serial','gps1', 'gps2']):
                configParsingInst.add_section(secNm)
                serialDataList = request.forms.getlist(secNm)
                configParsingInst.set(secNm, 'Device',serialDataList[0] )        
                configParsingInst.set(secNm, 'baudrate', serialDataList[1])
		configParsingInst.set(secNm, 'gpio', serialDataList[2])

        configParsingInst.write(configFile)
        configFile.close()
	procDataFrom = str(commands.getoutput("ps -aux | grep logger"))
	print "   " + procDataFrom
	proc_data = re.search(r"root\s+(\w+)", procDataFrom)
	print "   " + proc_data.group()
	print "   " + proc_data.group(1)
	
	os.system("kill -9 " + str(proc_data.group(1)))	
	#time.sleep(1)#wait for a second please
	os.system("python logger.py & ")
	os.system("ps -aux | grep logger &")

	redirect('/')

''' simple user login for future '''

@server.route('/login')
def login():
        return template('login')

@server.route('/login', method='POST')
def do_login():
        return template('login')        

BaseTemplate.defaults['route'] = request

run(server,reloader=True,host='192.168.0.127',port='8018',debug = True)

