import RPi.GPIO as GPIO
import time
import datetime
import os
from subprocess import call

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)
index = 0;
startmillis = int(round(time.time()))
pressed = False


def longPressed():
    print 'long press' 
    GPIO.output(16,False)
    GPIO.cleanup() # cleanup all GPIO 
    call(['mpg321','./mp3/XEX_ifva_Speech_Bye.mp3'])
    # call(['sudo' , 'shutdown', '-h', 'now'])
    exit()

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

    
    