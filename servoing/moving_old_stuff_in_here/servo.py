import os
import sys
import time
# import rasberry pi library
import RPi.GPIO as GPIO
sys.path.append('python/')
from lidar_lite import Lidar_Lite


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# pin 18, set as output, set to low initially
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
# creates PWM object with frequency of 50hz
pi_pwm = GPIO.PWM(13, 100)
pi_pwm.start(0)
# this sets pins to high
# GPIO.output(18, GPIO.HIGH)
# this sets pins to low
# GPIO.output(18, GPIO.LOW)
# time.sleep(1) to set pin high for 1 second
#lidar setup
counter = 0
while (1):
    
    print(counter)
    if (counter >= 100):
        counter = 0
        
    counter = counter + 1
    pi_pwm.ChangeDutyCycle(counter)