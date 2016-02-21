import time
import ConfigParser
import json
import paho.mqtt.client as mqtt
import os
import subprocess
import re
from subprocess import Popen
from pprint import pprint
import collections
from itertools import groupby
from operator import itemgetter
from collections import Counter
import re
from pprint import pprint
# load data


eventmap = []
key_status='status'
key_uuid='uuid'
key_files='files'
key_fileName='fileName'
# status never,playing,completed,status
never='never'
playing='playing'
completed='completed'
skipped='skipped'
MAX_LENGTH = 3
circularBuffer = collections.deque(maxlen=MAX_LENGTH)
appendCount=0
mqttclnt = None
conf = []
with open('eventmap.json') as data_file:
	eventmap = json.load(data_file)


def findProcess(processName):
	ps = subprocess.Popen("ps | grep " + processName,
						  shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.read()
	# print output
	ps.stdout.close()
	ps.wait()
	return output


def isProcessRunning(processName):
	output = findProcess(processName)
	# print "isProcessRunning : " +output
	if output.find(processName) != -1:
		return True
	else:
		return False

deviceID = ""
currentStatus = ""
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, rc):
	# print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("/lab3/ble/rssi/")

# The callback for when a PUBLISH message is received from the server.


def getEventMapFileName(eventmap, input_uuid):
	# print 'getEventMapFileName '+input_uuid
	fileName = "no file"
	for _data in eventmap:
		if(_data[key_uuid] == input_uuid) == True:
			if(_data[key_status]==never)==True:
				fileName = _data[key_files][0][key_fileName]
			elif(_data[key_status]==completed)==True:
				fileName = _data[key_files][1][key_fileName]
			elif(_data[key_status]==skipped)==True:
				fileName = _data[key_files][2][key_fileName]
			else:
				fileName = _data[key_files][0][key_fileName]
			
			print "playing file " + fileName
	return fileName


def playFile(filePath):
	print filePath
	if(os.path.isfile(filePath))==True:
		cmd = 'mpg321 ' + filePath + ' &'
		print cmd
		os.system(cmd)
	else :
		print "error open file :"+filePath



def getEventmapStatus(input_uuid):
	global eventmap
	for _data in eventmap:
		if (_data[key_uuid] == input_uuid) == True:
			return _data['status']
	return ""


def updateEventmapStatus(input_uuid, status):
	global eventmap
	output_uuid = None
	# print eventmap
	for _data in eventmap:
		if (_data[key_uuid] == input_uuid) == True:
			_data['status'] = status
			# print eventmap
			return _data['status']

# def most_common(lst):
# 	print lst
# 	return max(set(lst), key=lst.count)
def most_common(L):
	grouper = itemgetter("id")

	maxItem = max(L, key=lambda x:x['val'])
	
	# print "============maxItem============"
	# pprint(maxItem)
	# print "============maxItem============"

	result = []
	for key, grp in groupby(sorted(L, key = grouper), grouper):

		temp_dict = {'id': key, 'val': 0}
		temp_list = [float(item["val"]) for item in grp]
		temp_dict["qty"] = sum(temp_list)
		temp_dict["avg"] = temp_dict["qty"] / len(temp_list)
		temp_dict["val"] = temp_list
		result.append(temp_dict)

	averageMax = max(result, key=lambda x:x['avg'])
	print "============averageMax============"
	print averageMax["id"] + " | avg: " + str(averageMax["avg"])
	print "============averageMax============"
	return averageMax

def appendBuffer(input_uuid):
	global appendCount
	# print len(circularBuffer)
	output_uuid = None
	if(appendCount < MAX_LENGTH ):
		circularBuffer.append(input_uuid)
		appendCount+=1
		# print '------------------------------------'
		# print circularBuffer
		# most_common(circularBuffer)
		# print '------------------------------------'

	else:
		appendCount=0
		# output_uuid = circularBuffer
		
		print '====================================='
		output_uuid = most_common(circularBuffer)
		# print '---->>>>>>>>>>>>>>> : '
		# pprint(result)
		print '====================================='
		circularBuffer.clear()
	return output_uuid
def compairUUID(inputUUID="" , currentUUIDs=[]):

	for currentUUID in currentUUIDs:
		if(currentUUID==inputUUID):
			return True
		pass
	return False
def getUUIDFromEventMap(inputUUID="" , eventMap):
	global eventmap
	for _data in eventmap:
		currentUUIDs = _data[key_uuid];
		for currentUUID in currentUUIDs:
			if (currentUUID == input_uuid) == True:
				return currentUUIDs
			pass
	return None
def on_message(client, userdata, msg):
	# print(msg.topic+" "+str(msg.payload))
	obj = json.loads(msg.payload)
	global deviceID
	# print ('deviceID: ' + deviceID)
	# print ('obj[id]: ' + obj['id'])
	# print (deviceID == obj['id'])
	global eventmap
	global currentStatus
	# compair the current uuid
	# if uuid does not match skip the process
	
	value=float(obj['val'])
	obj['val']=value
	result = appendBuffer(obj)
	if mqttclnt and result:		
		mqttclnt.publish("/lab3/ble/result/", str(result['id']))
	if result:
		obj_uuid = result['id']
		
		if (compairUUID(deviceID , obj_uuid)) == None:
			if isProcessRunning('mpg321') == False:
				print "play track directly"
				deviceID = getUUIDFromEventMap(obj_uuid,eventmap)
				
				print 'event map status ' + getEventmapStatus(deviceID)
				currentStatus = getEventmapStatus(deviceID)
				if( currentStatus == 'never') == True:
					print 'never play'
					currentStatus = updateEventmapStatus(deviceID, 'playing')
				elif(currentStatus == 'playing') == True:
					print 'playing'
					currentStatus = updateEventmapStatus(deviceID, 'completed')
				elif(currentStatus== 'completed') == True:
					print 'paly completed note'
				elif(currentStatus == 'skipped') == True:
					print 'play skipped note'
					
				fileName = getEventMapFileName(eventmap, deviceID)
				playFile(fileName)
				print 'event map status ' + getEventmapStatus(deviceID)
			# else:
			# 	print "skip current track"
			# 	currentStatus = updateEventmapStatus(deviceID, 'skipped')
			# 	os.system('pkill mpg321')
			# 	deviceID = obj_uuid
			# 	if( currentStatus == 'never') == True:
			# 		print 'never play'
			# 		currentStatus = updateEventmapStatus(deviceID, 'playing')
			# 	fileName = getEventMapFileName(eventmap, obj_uuid)
			# 	playFile(fileName)
		else:
			if isProcessRunning('mpg321') == False:
				currentStatus = updateEventmapStatus(deviceID, 'completed')

def init():
	"""Read config file"""
	ret = {}
	config = ConfigParser.ConfigParser()
	config.read("config")
	global DEBUG
	DEBUG = True if int(config.get('Result', 'debug')) == 1 else False
	ret["url"]       = config.get('MQTT', 'url')
	ret["port"]      = int(config.get('MQTT', 'port'))
	ret["keepalive"] = int(config.get('MQTT', 'keepalive'))
	ret["result_id"]  = config.get('Result', 'result_id')
	return ret

def onConnect(client, userdata, rc):
	"""MQTT onConnect handler"""
	print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
	"""Init MQTT connection"""
	client = mqtt.Client()
	client.on_connect = onConnect
	try:
		client.connect(url, port, keepalive)
		client.loop_start()
		return client
	except Exception, e:
		print(e)
		return None

if __name__ == '__main__':
	conf = init()
	mqttclnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("localhost", 1883, 60)

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	client.loop_forever()

	# Non Blocking call interface
	# It starts a thread and is a more preferred method for use
	client.loop_start()