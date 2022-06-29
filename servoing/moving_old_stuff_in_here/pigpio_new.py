#import gpiozero
from gpiozero import Servo
from time import sleep

# hardware based library for servo motor
from gpiozero.pins.pigpio import PiGPIOFactory

# create new factory from previous import
factory = PiGPIOFactory()

# (Servo on pin 12, use this pin factory)
servo = Servo(12, pin_factory=factory)

# can also change the min_pulse, max_pulse
# even though the guy had the same sg90 servo motor
# datasheet says 1ms to 2ms gets you full range
# he had to change his to .5 to 2.5 to get full range
# servo = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# first time you run this program with PIGPIO library
# have to make sure servo component is working
# do they mean the hardware timer?
# run this command on the terminal. inside same directory


# sudo pigpiod
# the d means its running as a background process now


print("Start in the middle")
servo.mid()
sleep(3)
print("Go to min")
servo.min()
sleep(3)
print("Go to max")
servo.max()
sleep(3)
print("And back to middle")
servo.mid()
sleep(3)
servo.value = None

