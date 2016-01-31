import time, ConfigParser, json
import paho.mqtt.client as mqtt
import os
import subprocess
import re
from subprocess import Popen

def findProcess( processName ):
	ps = subprocess.Popen("ps | grep "+processName, shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.read()
	# print output
	ps.stdout.close()
	ps.wait()
	return output
def isProcessRunning( processName):
	output = findProcess( processName )
	# print "isProcessRunning : " +output
	if output.find(processName) != -1:
		return True
	else:
		return False

deviceID = ""
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	# print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("/lab3/ble/nearest/")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	obj = json.loads(msg.payload)
	global deviceID
	# print ('deviceID: ' + deviceID)
	# print ('obj[id]: ' + obj['id'])
	# print (deviceID == obj['id'])
	if (deviceID == obj['id']) == False :
		deviceID = obj['id']
		if deviceID == "fc:ac:48:93:85:07":
			print("do this>>>>>>>>>");
			if isProcessRunning('omxplayer') == False:
				os.system('omxplayer /home/pi/example/mp3s/Chapter_1.mp3 &')
			# play mp3s/chapter1
			##do this
		if deviceID == "e6:04:aa:bd:67:d2":
			print("do that---------");
			if isProcessRunning('omxplayer') == False:
				os.system('omxplayer /home/pi/example/mp3s/Chapter_2.mp3 &')
			#do that
			# play mp3s/chapter3

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

#Non Blocking call interface
#It starts a thread and is a more preferred method for use
client.loop_start()