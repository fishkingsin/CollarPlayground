import RPi.GPIO as GPIO
import time
import datetime
from Adafruit_7Segment import SevenSegment
import os

GPIO.setmode(GPIO.BCM)
segment = SevenSegment(address=0x70)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        segment.writeDigit(0,0)
        segment.writeDigit(0,0)
        segment.writeDigit(0,0)
        segment.writeDigit(0,1)
        time.sleep(0.2)
    else:
    	segment.writeDigit(0,0)
        segment.writeDigit(0,0)
        segment.writeDigit(0,0)
        segment.writeDigit(0,2)