#!/usr/bin/python

import thread
import time
import datetime
from Adafruit_7Segment import SevenSegment
import os
import rx
from rx.subjects import Subject
from rx import Observable, Observer
import RPi.GPIO as GPIO
from subprocess import call
LIMIT = 1800000
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
# LIMIT = 65000
# LIMIT = 10000
current_second=0
GPIO.output(16,False)

def bi_time( threadName, delay):
	GPIO.output(16,True)
	time.sleep(delay);
	GPIO.output(16,False)

def startThread(delay):
	try:
		thread.start_new_thread( bi_time, ("Thread-1", delay, ) )
	except:
		print "Error: unable to start thread"
	
class BuzzerObserver(Observer):
		def on_next(self, x):
			if(x%60==0):
				startThread(2);
			elif (x < 60 and x%10==0 and x != 10):
				startThread(1);
			elif (x<=10):
				startThread(0.5);
			
			# print("Got: %s" % x)
		def on_error(self, e):
			print("Got error: %s" % e)
				
		def on_completed(self):
			print("Sequence completed")
			call(['pkill' , 'python']);
			exit()
stream = Subject()
stream.subscribe(BuzzerObserver())
# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment(address=0x70)

print "Press CTRL+Z to exit"
startmillis = int(round(time.time() * 1000))
# Continually update the time on a 4 char, 7-segment display
while(True):
	currentmillis = int(round(time.time() * 1000))
	# now = datetime.datetime.now()
	# hour = now.hour
	diff = LIMIT-int(currentmillis - startmillis)
	second = diff/1000
	minute = second/60
	if(current_second!=second):
		stream.on_next(second)
		current_second=second
	if(minute>0):
		segment.writeDigit(0, int(minute / 10))     # Tens
		segment.writeDigit(1, minute % 10)          # Ones
		# Set minutes

		segment.writeDigit(3, int(second % 60 / 10 ))   # Tens
		segment.writeDigit(4, second % 60 % 10)        # Ones
		
	else:
		segment.writeDigit(0, int((diff / 1000)/10))    # Tens
		segment.writeDigit(1, int((diff / 1000)%10))          # Ones
		
		segment.writeDigit(3, int(diff / 100)%10 )   # Tens
		segment.writeDigit(4, int(diff % 10 ) )        # Ones
	# Toggle colon
	segment.setColon(second % 2)              # Toggle colon at 1Hz
	
	if(currentmillis>startmillis+LIMIT):
		# should fire timeout
		stream.on_completed();
		# startmillis = currentmillis;

	time.sleep(0.01)
