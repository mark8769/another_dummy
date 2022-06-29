from gpiozero import Servo
from time import sleep



servo = Servo(12)
servo_two = Servo(13)
val = -1
neg = -0.1
pos = 0.1
modifier = pos
              
while True:
# 
#     if val > 1:
#         val = 1
#         modifier = neg
#     if val < -1:
#         val = -1
#         modifier = pos
#     
#     print(val)
#     servo.value = val
#     val = val + modifier
#     sleep(.01)
    
    print("Servo value 1")
    servo.value = 1
    sleep(1)
    print("Servo vaLUE 0")
    servo.value = 0
    sleep(1)
    print("Servo vALUE -1")
    servo.value = -1
    sleep(1)
    print("Servo value 0")
    servo.value = 0
    sleep(1)