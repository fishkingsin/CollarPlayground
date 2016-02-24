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
# LIMIT = 10000
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# LIMIT = 65000

current_second=0
GPIO.output(16,False)

def bi_time( threadName, delay):
	if delay == 10:
		print("Sequence completed")
		time.sleep(2);
		GPIO.output(16,True)
		time.sleep(10);
		GPIO.output(16,False)
		
		call(['mpg321', './mp3/XEX_ifva_Speech_Time.mp3' ,'&'])
		call([ 'shutdown', '-h', 'now']);
		exit()
	else :
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
			if(x > 60 and x%60*5==0):
				startThread(1);
			elif (x < 60 and x%10==0 and x != 10):
				startThread(1);
			elif (x<=10):
				startThread(0.5);
			
			# print("Got: %s" % x)
		def on_error(self, e):
			print("Got error: %s" % e)
				
		def on_completed(self):
			startThread(10);
			
stream = Subject()
stream.subscribe(BuzzerObserver())
# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment(address=0x70)
currentmillis = 0
# print "Press CTRL+Z to exit"
startmillis = int(round(time.time() * 1000))
# Continually update the time on a 4 char, 7-segment display
pressed = False
pressStartmillis = 0
def longPressed():
	print 'long press' 
	GPIO.cleanup() # cleanup all GPIO 
	call(['mpg321','./mp3/XEX_ifva_Speech_Bye.mp3'])
	# call(['sudo' , 'shutdown', '-h', 'now'])
	exit()

while(True):
	if(currentmillis<startmillis+LIMIT):
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

		
	input_state = GPIO.input(18)
	if input_state == False:
		if(pressed == False):
			pressStartmillis = time.time()*1000
		pressed = True;
		
		# time.sleep(0.2)
		
	else:
		if(pressed):
			pressCurrentmillis = time.time()*1000
			diff  = (pressCurrentmillis - pressStartmillis)/1000.0
			print diff
			if( diff > 3 ):
				longPressed()
			elif ( diff > 0 and diff <2  ):
				shortPressed()
			pressed = False;

	time.sleep(0.01)
