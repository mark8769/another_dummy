from piservo import Servo
import time

myservo = Servo(13)


while True:
    print("I am in the loop")
    myservo.write(180)
    time.sleep(2)
    myservo.write(90)
    time.sleep(2)
    myservo.write(0)
    time.sleep(2)
    myservo.write(90)
    time.sleep(2)