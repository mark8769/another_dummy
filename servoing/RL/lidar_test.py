# trying this from stack overflow
import sys
from gpiozero import Servo
import math
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from obs_two_pass import set_servo_angle
sys.path.append('python/')
from lidar_lite import Lidar_Lite
# set up PiGPIOFactory to use hardware and not software pwm
factory = PiGPIOFactory()
hitec_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)

lidar = Lidar_Lite()
connected = lidar.connect(1)
    
temp_input = None
temp_distance = 0
while (True):
    
    temp_input = int(input("Enter in an angle: "))
    set_servo_angle(temp_input, hitec_servo)
    sleep(.06)
    print(lidar.getDistance())
        
    
    