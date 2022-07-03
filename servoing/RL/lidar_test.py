'''
lidar_test.py

Created - Mark Ortega-Ponce

7/x/2022

Purpose: Helper file to get the correct measurements from the lidar sensor.
        During testing, I found that I was picking up the measurement from
        previous angle and saving it to the new angle. Eg. I set the motor angle,
        take the measurement from the lidar sensor, save prev angle in curr. angle.

        Solution was to add some delay after setting motor angle, since we are using this in
        RL we want to reduce the amount of sleep time to as low as we can. Time asleep
        can be reduced the smaller jumps in angle you make, the bigger the jumps the more
        sleep time is needed.

        Example information: current angle = 20, distance = 40

        set_motor_angle(50)

        angle_50_distance = get_distance()
        print(angle_50_distance) --> 40
        set_motor_angle(20)
        angle_20_distance = get_distance()
        print(angle_20_distance) --> 100
'''
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
#Edit July something
# prev min .45, prev max = 2.45
# Hitec datasheet found in some box, conveniently using same servo
hitec_servo = Servo(12, min_pulse_width=.58/1000, max_pulse_width=2.38/1000, pin_factory=factory)
lidar = Lidar_Lite()
connected = lidar.connect(1)
    
temp_input = None
temp_distance = 0
while (True):
    
    temp_input = int(input("Enter in an angle: "))
    set_servo_angle(temp_input, hitec_servo)
    sleep(.06)
    print(lidar.getDistance())
        
    
    