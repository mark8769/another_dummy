# trying this from stack overflow
import sys
from gpiozero import Servo
import math
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
sys.path.append('python/')

# set up PiGPIOFactory to use hardware and not software pwm
factory = PiGPIOFactory()
# set up servo, GPIO pin 12, min_pulse = .45ms, max_pulse = 2.45ms, use hardware
# https://hitecrcd.com/files/Servomanual.pdf
hitec_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)

from lidar_lite import Lidar_Lite


def set_servo_angle(angle, servo):
    # we have -1 to 1
    # we have range of (0, 2)
    # servo range is from (0, 180)
    # if we do 2 / 180
    # we have 0.01111111111111
    value = angle * 0.01111
    #print(angle)
    #print(value)
    if value < -1:
        value = -1
    
    if value > 1:
        value = 1
        
    servo.value = value

lidar = Lidar_Lite()
connected = lidar.connect(1)

if connected < -1:
    print ("Not Connected")
else:
    print("Connected")
    
temp_input = None
temp_distance = 0
while (True):
    
    temp_input = int(input("Enter in an angle: "))
    set_servo_angle(temp_input, hitec_servo)
    sleep(.06)
    print(lidar.getDistance())
        
    
    