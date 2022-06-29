from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep

# s = Servo(26)
# while (True):
#     
#     s.min()
#     sleep(2)
#     s.max()
#     sleep(2)

servo = AngularServo(12, min_pulse_width=0.45/1000, max_pulse_width=2.45/1000)
servo_two = AngularServo(13, min_pulse_width=1.0/1000, max_pulse_width=2.0/1000)
counter = -90

while (True):
    servo.angle = counter
    sleep(.3)
    servo_two.angle = counter
    print(counter)
    
    if (counter == 90):
        while (counter >= -90):
            servo.angle = counter
            servo_two.angle = counter
            sleep(.3)
            print(counter)
            counter -= 5
    
    counter += 5
#     print("Moving to 90")
#     servo.angle = 90
#     sleep(2)
#     print("Moving to 0")
#     servo.angle = 0
#     sleep(2)
#     print("Moving to -90")
#     servo.angle = -90
#     sleep(2)

# servo angle must be -90 to 90
# for i in range(-90, 91):
#     servo.angle = i
#     sleep(1)
