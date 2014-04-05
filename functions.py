import commands
import re
import datetime

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def runThisCommand( cmd ):
	return str(commands.getoutput(cmd))

def getRequiredFieldData( sCommandPlease ):

    yourDataRes = {
        'upTime': getTheUpTimePlease(),
        'curtime': getTheCurTimePlease(),
        'kernel': getTheKernelPlease(),
        'host':getTheHostNamePlease(),                
        'totalSpace':getToTalSpacePlease(),
        'freeSpace':getFreeSpacePlease(),
        'usedSpace':getUsedSpacePlease(),
        'ipaddr':getTheIpAddrPlease(),
        'netMask': getTheNetMaskPlease()
        }[sCommandPlease]
    return yourDataRes

def getTheUpTimePlease():
       
    uptime_fromHere = str(commands.getoutput('cat /proc/uptime') )    ## redirecting o/p channel and taking directly in from here.
    varForTimeNow = re.search( r"[0-9]+", uptime_fromHere)        
    m, s = divmod(int(varForTimeNow.group()), 60)
    h, m = divmod(m, 60)
    varForTime = "%d:%d:%d" %(h,m,s)
    return varForTime

def getTheCurTimePlease():

    uptime_fromHere = str(commands.getoutput('uptime') )    ## redirecting o/p channel and taking directly in from here.
 
    varForNow = re.search(r"([0-9]+:[0-9]+:[0-9]+)", uptime_fromHere)
    
    return varForNow.group()#time

def getTheKernelPlease():

    Data_fromHere = str(commands.getoutput('uname -r'))
    #varForNow = re.search(r"(\w+)\s+(\w+)\s+(\w+.\w+.\w+-\w+-\w+\w+?)", Data_fromHere)
        
    return ": %s"%(Data_fromHere)

def getTheHostNamePlease():
    Data_fromHere = str(commands.getoutput('uname -n'))
    #varForNow = re.search(r"(\w+)\s+(\w+)\s+(\w+.\w+.\w+-\w+-\w+\w+?)", Data_fromHere)        

    return Data_fromHere

def getToTalSpacePlease():

    varData_Temp = str(commands.getoutput('df -h ./ | grep root'))          # this will give a single line output as it is been requested for the current path.
    varForNow = re.search (r"(([0-9]+)\w+)\s+(([0-9]+)\w+)\s+(([0-9]+)\w+)",varData_Temp)
            
    return varForNow.group(1)

def getFreeSpacePlease():
    varData_Temp = str(commands.getoutput('df -h ./ | grep root'))          # this will give a single line output as it is been requested for the current path.
    varForNow = re.search (r"(([0-9]+)\w+)\s+(([0-9]+)\w+)\s+(([0-9]+)\w+)",varData_Temp)
    
    return  varForNow.group(5)

def getUsedSpacePlease():
    
    varData_Temp = str(commands.getoutput('df -h ./ | grep root'))          # this will give a single line output as it is been requested for the current path.
    varForNow = re.search (r"(([0-9]+)\w+)\s+(([0-9]+)\w+)\s+(([0-9]+)\w+)",varData_Temp)
    
    return varForNow.group(3)    

def getTheIpAddrPlease():

    varData_Temp = str(commands.getoutput('ifconfig'))
    varForNow = re.search(r"addr:(\w+.\w+.\w+.\w+)", varData_Temp)

    return varForNow.group(1)

def getTheNetMaskPlease():

    varData_Temp = str(commands.getoutput('ifconfig'))
    varForNow = re.search(r"Mask:(\w+.\w+.\w+.\w+)", varData_Temp)

    return varForNow.group(1)

def isProcessorType():
    str_procName = str(commands.getoutput('uname -m | grep arm'))

    if str_procName != "":
        IsArmProcessor__ = 1
    else:
        IsArmProcessor__ = 0
    
    return IsArmProcessor__
