import RPi.GPIO as GPIO
import time
import datetime
from Adafruit_7Segment import SevenSegment
import os
from subprocess import call

GPIO.setmode(GPIO.BCM)
segment = SevenSegment(address=0x70)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)
index = 0;
startmillis = int(round(time.time()))
pressed = False

call(['unlink' , 'mp3'])
call(['ln','-s' , './chi',  'mp3' ])
call(['ls' , './mp3'])
index = 0
segment.writeDigit(0,0)
segment.writeDigit(1,0)
segment.writeDigit(2,0)
segment.writeDigit(3,0)
segment.writeDigit(4,1)

def longPressed():
    print 'long press' 
    GPIO.output(16,False)
    GPIO.cleanup() # cleanup all GPIO 
    print 'exit'
    exit()
def shortPressed():
    global index
    print 'short press'
    if(index == 1):
        call(['unlink' , 'mp3'])
        call(['ln','-s' , './chi',  'mp3' ])
        call(['ls' , './mp3'])
        index = 0
        segment.writeDigit(0,0)
        segment.writeDigit(1,0)
        segment.writeDigit(2,0)
        segment.writeDigit(3,0)
        segment.writeDigit(4,1)
    elif (index == 0):
        call(['unlink' , 'mp3'])
        call(['ln','-s' , './eng',  'mp3' ])
        call(['ls' , './mp3'])
        index = 1
        segment.writeDigit(0,0)
        segment.writeDigit(1,0)
        segment.writeDigit(2,0)
        segment.writeDigit(3,0)
        segment.writeDigit(4,2)
while True:
    input_state = GPIO.input(18)
    if input_state == False:
        if(pressed == False):
            startmillis = time.time()*1000
        pressed = True;
        
        time.sleep(0.2)
        GPIO.output(16,True)
    else:
        if(pressed):
            currentmillis = time.time()*1000
            diff  = (currentmillis - startmillis)/1000.0
            print diff
            if( diff > 3 ):
                longPressed()
            elif ( diff > 0 and diff <2  ):
                shortPressed()
            pressed = False;
        GPIO.output(16,False)

    
    