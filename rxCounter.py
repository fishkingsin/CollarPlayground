#!/usr/bin/python

import time
import datetime
import rx
from rx import Observable, Observer
from Adafruit_7Segment import SevenSegment


# LIMIT = 1800000
LIMIT = 65000
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
    startmillis = currentmillis;
  time.sleep(0.001)
