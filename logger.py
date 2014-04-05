import ConfigParser
import os, sys, commands
import threading
from time import sleep
import serial
import signal
import functions

openPortFlag = 1# always On
class allPortDevice(threading.Thread):
        
        def __init__(self, mgpioLed, isOnState):
                threading.Thread.__init__(self)
                self.isState = isOnState
                self.gpioNum = mgpioLed
                
        def run(self):

                try:
			#print "now Trying code from here"
                	__IsArmProcessor__ = functions.isProcessorType()                        
			#print "    " + str( __IsArmProcessor__ )
                        # on the led state of Led 1
                	if (int(__IsArmProcessor__) != 0):
				import RPi.GPIO as GPIO_RPI                                
				#GPIO_RPI.setwarnings( Flase )
				GPIO_RPI.setmode( GPIO_RPI.BOARD )
				GPIO_RPI.setwarnings( 0 )
                        	GPIO_RPI.setup(int(self.gpioNum), GPIO_RPI.OUT )
                        	GPIO_RPI.output(int(self.gpioNum), int(self.isState))
                                # isState is 1, true, High.change thsi data according to led config. high or low.
				# alwasy on till this thread is on
			else:
                		print "This is always on till port is open, Identified as this script is not running on Raspberry Pi."
		except:
			print "Something goes wrong"
			print sys.exc_info()
                             

class logger_thread(threading.Thread):
	
	
	def __init__(self, port, baudrate, dumpfile):
		threading.Thread.__init__(self)
		self.port = port
		self.baudrate = baudrate
		self.dumpfile = dumpfile
		

	def run(self):
		global openPortFlag 
		try:
			baud = int(baudrate)
		except:
			baud = 115200
		
		try:
			# timeout is necessary
			#print openPortFlag
			infile = serial.Serial(self.port, baud, timeout=1)
			openPortFlag = 1
			print "      " + self.dumpfile+" : Port opened successfully which is on port" + self.port
		except:
			print "      " + self.dumpfile+": Device not detected on  " + self.port
			openPortFlag = 0 #false
			#print "      " + str( openPortFlag )
			# infile = os.open("/dev/ttyUSB0", os.O_NONBLOCK | os.O_RDONLY)
			# print "opening /dev/ttyUSB0 for now"
			return

		try:
			outfile = open(os.path.join("./logs/", self.dumpfile+".log"), "a+")
			
		except:
			print "   " + self.dumpfile+":Error opening output file"
			return

		buf=''
		tmplen = 0
		return_flag = False
		while True:
			tmp = infile.read(100)
			tmplen = tmplen + len(tmp)
			buf = ''.join([buf, tmp])
			if tmplen > 4096*4:
				written = outfile.write(buf)
				tmplen = 0
				buf=''
			else:
				pass

			if not lock.acquire(False):
				pass
			else:
				try:
					print self.dumpfile+": acquired lock, finishing now."
					outfile.write(buf)
					tmplen = 0
					buf=''
					infile.close()
					outfile.close()
					return_flag = True
				finally:
					lock.release()

			if return_flag == True:
				return

class logNow(threading.Thread):

	def __init__(self, port, baudrate, dumpfile):
		threading.Thread.__init__(self)
		self.port = port
		self.baudrate = baudrate
		self.dumpfile = dumpfile

	def run(self):
		global openPortFlag 
		try:
			baud = int(baudrate)
		except:
			baud = 115200
		
		try:
			# timeout is necessary
			#print openPortFlag
			infile = serial.Serial(self.port, baud, timeout=1)
			openPortFlag = 1
			print "      " + self.dumpfile+" : Port opened successfully which is on port" + self.port
		except:
			print "      " + self.dumpfile+": Device not detected on  " + self.port
			openPortFlag = 0 #false
			#print "      " + str( openPortFlag )
			# infile = os.open("/dev/ttyUSB0", os.O_NONBLOCK | os.O_RDONLY)
			# print "opening /dev/ttyUSB0 for now"
			return

		try:
			outfile = open(os.path.join("./logs/", self.dumpfile+".log"), "a+")
			
		except:
			print "   " + self.dumpfile+":Error opening output file"
			print sys.exc_info()
			return

		buf=''
		tmplen = 0
		return_flag = False

		tmp = infile.read(100)
		tmplen = tmplen + len(tmp)
		buf = ''.join([buf, tmp])
		print 'execution point goes from here...'
		#buf.join("this is from my side")
		buf = buf + "Writting to file now."		
		if tmplen > 4096*4:
			written = outfile.write(buf)
			tmplen = 0
			buf=''
		else:
			if tmplen > 0:
				writtem = outfile.write(buf)
				tmplen = 0
				buf = ''
				print 'Written whatever left in buffer to respective file'
			else:
				print 'Buffer is empty hence nothing to write.'

		# just write for once and exit from thread, hence no thread will be left running.
		tmplen = 0
		buf=''
		infile.close()
		outfile.close()
		return_flag = True
		return


def signal_handler(signal, frame):
	print 'You pressed Ctrl+C'
	lock.release()
	# takes upto 1 second per thread to exit, because of serial timeout
	sys.exit(0)

def writeBeforeDownload_Handler(signal, frame):
	print 'signal received to write on log now, one by one...'
	## call logger thread for log and then download.
	try:
		config = ConfigParser.ConfigParser()
		config.read('settings.cfg')#this closes the config file after read.
	except:
		print ' settngs.cfg file not found or opended already.'
		print sys.exc_info()

	for section in config.sections():
		port = ''
		dumpfile = ''
		try:
			port = config.get(section, 'device')
		except:
			continue
		try:
			baudrate = config.get(section, 'baudrate')
		except:
			baudrate =115200
		try:
			gpioOf = config.get(section, 'gpio')
		except:
			continue

		t = logNow(port, baudrate, section)
		t.start()
		# shoot thread and let them write...one by one.
		#this thread exits after writting to file from buffer.


if __name__ == "__main__":
	# Main Runtime parse config and dump in file
	#print "this is Logger"
	signal.signal(signal.SIGINT, signal_handler)
	# user defined signal for triggering the specified procedure.
	signal.signal(signal.SIGUSR1, writeBeforeDownload_Handler)

	try:
		theProcessor = functions.isProcessorType()
		#print "     " + str( theProcessor )
		sleep( 5 )
		if( theProcessor == 1):
			import RPi.GPIO as gpio_s
			#print "Cleaning up board"		
			gpio_s.setmode( gpio_s.BOARD )
			gpio_s.setwarnings( 0 )
			gpio_s.cleanup()
			sleep( 5 )
	except:
		print sys.exc_info()
		time.sleep( 2 )
	try:
		config = ConfigParser.ConfigParser()
		config.read('settings.cfg')
	except:
		print '     settings.cfg not found in current drive. Please place settings.cfg at correct place.'
		print sys.exc_info()

	thread_list = []
	gpioLED_list = []
	
	lock = threading.Lock()
	try:
		lock_status = lock.acquire()
		if lock_status == False:
			print "Error could not acquire lock, will not be able to stop threads"
	except:
		print "Error could not acquire lock, will not be able to stop threads"
		print sys.exc_info()

	try:	
		for section in config.sections():
			port = ''
			dumpfile = ''
			try:
				port = config.get(section, 'device')
			except:
				continue
			try:
				baudrate = config.get(section, 'baudrate')
			except:
				baudrate =115200
			try:
				gpioOf = config.get(section, 'gpio')
			except:
				continue

			t = logger_thread(port, baudrate, section)
			t.start()
			thread_list.append(t)
			sleep( 2 )
			#print "     " + gpioOf
			#print "     " + str(openPortFlag)
			#print "     " + port
			if openPortFlag == 1:
				th = allPortDevice(gpioOf, 0)
				th.start()
				gpioLED_list.append(th)
			elif openPortFlag == 0:
				th = allPortDevice( gpioOf, 1 )
				th.start()
				gpioLED_list.append(th)
	except:
		print '      something went wrong, may be any section is not found in config file.'
		print sys.exc_info()		

	while True:		
		signal.pause()		                        
		pass
