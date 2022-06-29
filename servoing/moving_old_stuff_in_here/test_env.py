import os
import sys
import time
from time import sleep
import random
sys.path.append ("../")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import blob
import drive
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

rvr = SpheroRvrObserver()

# NOTE: Can we store the actions and run in reverse to reset the robot??
# NOTE: Or reverse for some time and then randomly orient to reset?
# 
# STATES (26 of them) -- more when we start to look at size and/or distance
# Lay a 5x5 grid over the frame, which is 5x5=25 states + 1 more for if the blob is not visible
# ACTIONS (6 of them)
# HL,L,S,R,HR (Hard Left to Hard Right) 

#rawMotors(left_mode, left_speed, right_mode, right_speed). mode={stop,forward,reverse}
full_speed = 255
duty_cycle = 1/8

speed = int(full_speed*duty_cycle)

vision = blob.PiBlob()
while True:
    vision.capture()
    vision.find_blob()
    print("BLOB",vision.blob[0])

class ServoingEnvironment:

    def __init__(self) -> None:

        self.actions = [
            ["left",500], ["left", 300], ["left",150], ["fwd",150],
            ["right",500], ["right", 300], ["right",150] ]

        self.num_of_actions = len(self.actions)
        self.num_of_states = 11

        self.no_blob = self.num_of_states - 1     # signifies blob is not in the visual field
        self.reward_state = (self.num_of_states-1)//2    # in the middle
        self.current_state = self.no_blob
        vhandle = threading.Thread(target = visual.main)
        vhandle.start()
        
    def reset(self):
        # Put the robot in a starting position.
        print("RVR being reset")
        return self.get_state()

    def get_state(self):
        # Retrieve y-position of the blob
        #return random.randint(0,self.num_of_states)
        return visual.get_y_value()
        print(y_value, "This is being returned?")
        #width = 480
        #blob = pi.get_blob()
        #state =  (self.num_of_states / width) * y
        #self.current_state = blob[1]
        #return state

    # s1,r,d = env.step(a)
    def step(self,action):
        # Send action command to robot and get next state.
        driveParams = self.actions[action]
        drive.drive(driveParams[0], driveParams[1])
        sleep(2)  # delay for 2 seconds to let it drive
        new_state = self.get_state()
        reward = 0
        done = False
        if (new_state == self.reward_state):
            reward = 1
            done = True    # reached goal. done
        elif (new_state == self.no_blob):
            done = True    # failed. done.
        else:
            reward = 0
        return new_state, reward, done



