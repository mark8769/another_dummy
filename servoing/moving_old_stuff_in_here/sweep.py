from gpiozero import Servo
import math
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

#sg_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)
# need to change the pulse width, gets most of range, use this for tilting? Can also look for full range
# will probably have to, so I can specify specific angles
#futaba_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)
# currently this pulse width works great with this servo, full 180 motion
hitec_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)
flag = True
while flag:
    print("I should be sweeping")
    for i in range(0, 360):
    # use sin wave, (-1, 1), 0 being center, convert to radians
        print(i)
        
#         if i == 90:
#             print(i)
#             print(math.sin(math.radians(i)))
#             flag = False
#             break
        # servo values should be in range of (-1,1)
        #sg_servo.value = math.sin(math.radians(i))
        #futaba_servo.value = math.sin(math.radians(i))
        hitec_servo.value = math.sin(math.radians(i))
        print(hitec_servo.value)
        sleep(.01)


def servo_angle(angle: int):
    pass
    
    