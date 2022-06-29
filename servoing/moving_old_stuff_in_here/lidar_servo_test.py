from gpiozero import Servo
import math
from time import sleep
import sys
from gpiozero.pins.pigpio import PiGPIOFactory
# get lidar_lite file from python folder
sys.path.append('python/')
from lidar_lite import Lidar_Lite
# set up PiGPIOFactory to use hardware and not software pwm
factory = PiGPIOFactory()
# set up servo, GPIO pin 12, min_pulse = .45ms, max_pulse = 2.45ms, use hardware
hitec_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)
# set up lidar lite
lidar = Lidar_Lite()
# check if lidar is connected
connected = lidar.connect(1)

if connected < -1:
    print ("Not Connected")
else:
    print("Connected")

counter = -90
counter_helper = 5
lidar_distance = None
prev_distance = None

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

while True:
    # servo goes from (-90, 90)
    # if we get past 90 want to sweep back
    if counter > 90:
        counter_helper = -5
    # if we get past -90 want to sweep back
    
    if counter < -90:
        counter_helper = 5
        
    set_servo_angle(counter, hitec_servo)
    lidar_distance = lidar.getDistance()
    print(lidar_distance)
    
    # if we get a bad reading, want to do take reading again
    # keep getting readings until we dont get -1
    # reduces some noise
    while lidar_distance == -1:
        prev_distance = lidar_distance
        lidar_distance = lidar.getDistance()
        print("--------------------")
        print("Got stuck")
        print("Counter: ", counter)
        print("Prev Distance: ", prev_distance)
        print("New Distance: ", lidar_distance)
        print("--------------------")
        sleep(.5)
        
    counter += counter_helper
    sleep(.1)


