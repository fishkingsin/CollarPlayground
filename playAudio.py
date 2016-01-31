import os
import subprocess
import re
from subprocess import Popen
# os.system('omxplayer /home/pi/example/mp3s/Chapter_3.mp3 &')

def findProcess( processName ):
	ps = subprocess.Popen("ps | grep "+processName, shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.read()
	print output
	ps.stdout.close()
	ps.wait()
	return output
def isProcessRunning( processName):
	output = findProcess( processName )
	print "isProcessRunning : " +output
	if output.find(processName) != -1:
		return True
	else:
		return False

print(isProcessRunning('omxplayer'))