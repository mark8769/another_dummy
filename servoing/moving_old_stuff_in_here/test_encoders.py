import os
import sys
import time


sys.path.append('python/')
from lidar_lite import Lidar_Lite

# add another ../ to go back another directory from having gone into /python
sys.path.append('../../')
sys.path.append('../..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# import RVR stuff, needed for simple set up
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

# import RVR led libraries
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups

# in range from 0 to 255
MAX_SPEED = 128
# default speed
SPEED = 70

rvr = SpheroRvrObserver()

def get_encoder_counts_response_handler(response):
    print("Encoder counts response: ", response)


def drive(dir):

    print(dir)

    if (dir=="right"):
        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,   
            left_duty_cycle = 128,
            right_mode=RawMotorModesEnum.reverse.value,
            right_duty_cycle= 128
        )
    elif(dir == "left"):
        rvr.raw_motors(
            left_mode=RawMotorModesEnum.reverse.value,   
            left_duty_cycle = SPEED,
            right_mode=RawMotorModesEnum.forward.value,
            right_duty_cycle = SPEED
        )
    # no sensors in the back of our rover, so should go slow
    elif(dir == "reverse"):
        rvr.raw_motors(
            left_mode=RawMotorModesEnum.reverse.value,   
            left_duty_cycle = 60,
            right_mode=RawMotorModesEnum.reverse.value,
            right_duty_cycle = 60
        )
    elif(dir == "forward"):
        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,   
            left_duty_cycle = SPEED,
            right_mode=RawMotorModesEnum.forward.value,
            right_duty_cycle = SPEED
        )
        
        
def drive_second():
    #this is a simple code to run the wheels of the RVR forward
    
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(1)

    rvr.reset_yaw()
    
    rvr.set_custom_control_system_timeout(command_timeout=200)  
    
    print("test1")
    
    rvr.raw_motors(
            # could be adjusted to move in the reverse direction by changing forward to reverse
            left_mode=RawMotorModesEnum.reverse.value,   
            left_duty_cycle = 140,  # Valid duty cycle range is 0-255, 140 before
            right_mode=RawMotorModesEnum.forward.value,
            right_duty_cycle = 140  # Valid duty cycle range is 0-255, 140 before
    )
    print("test2")
    rvr.close()


def set_both_front_leds(red, green, blue):
    
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_right.value,
        led_brightness_values=[red, green, blue]
    )
    
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_left.value,
        led_brightness_values=[red, green, blue]
    )
    
def set_right_led(red, green, blue):
    
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_right.value,
        led_brightness_values=[red, green, blue]
    )
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_right.value,
        led_brightness_values=[255, 0, 0]
    )


def main():
    
    # examples all have it enclosed try block
    try:
        rvr.wake()
        # give rover time to wake up
        time.sleep(2)
        # resets current orientation / position (x, y, z values?)
        rvr.reset_yaw()
        #lidar setup
        lidar = Lidar_Lite()
        connected = lidar.connect(1)

        if connected < -1:
            print("Lidar not connected, check connections")

        
        while(1):
            
            distance_from_object = lidar.getDistance()
            print(distance_from_object)
            print("forward 2 sec delay")
            drive("forward")
            time.sleep(2)
            rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)
            print("reverse 2 sec delay")
            drive("reverse")
            time.sleep(2)
            rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)
            print("forward 1 sec delay")
            time.sleep(1)
            rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)
            print("forward .5 sec delay")
            time.sleep(.5)
            rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)

            rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)
            time.sleep(5)
            
    except KeyboardInterrupt:

        print("Program terminated with keyboard interrupt\n")

    finally:
        # always close the rover like a file, or buffer, or something
        rvr.close()
    
            
if __name__ == '__main__':
    main()
     