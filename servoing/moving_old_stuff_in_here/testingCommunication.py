import os
import sys
import time
# import rasberry pi library
import RPi.GPIO as GPIO
sys.path.append('python/')
from lidar_lite import Lidar_Lite
# setting the mode for the gpio pin
# can either do BCM or board
# BCM = Numbering system you see on the actual pins
# Board = NUmbering system is 1, 2, 3, ... 40
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# pin 18, set as output, set to low initially
# set this to low as our OE pin on the level shifter
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
# 23 will be our voltage we want converted
# at 0 we get 0 voltage
# at 3.3v we get 5v out from the level shifter
# start with motor off
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
# creates PWM object with frequency of 50hz
#pi_pwm = GPIO.PWM(13, 100)
#pi_pwm.start(0)
# this sets pins to high
# GPIO.output(18, GPIO.HIGH)
# this sets pins to low
# GPIO.output(18, GPIO.LOW)
# time.sleep(1) to set pin high for 1 second
#lidar setup
lidar = Lidar_Lite()
connected = lidar.connect(1)


while (1):
    counter = 50
    print(lidar.getDistance())
    GPIO.output(23, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(23, GPIO.LOW)
    time.sleep(2)
    #counter = counter + 1
    
    #if (counter >= 100):
        #counter = 0
    #pi_pwm.ChangeDutyCycle(counter)
    #time.sleep(.01)