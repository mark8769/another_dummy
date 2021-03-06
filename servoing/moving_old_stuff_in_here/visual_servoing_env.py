import os
import sys
import time
from time import sleep
import random

sys.path.append ("../..")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import blob
import drive

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

rvr = SpheroRvrObserver()

# NOTE: Can we store the actions and run in reverse to reset the robot??
# NOTE: Or reverse for some time and then randomly orient to reset?
# 
# STATES (12)
# - the pixel width of the image is divided into 11 states
# - the 12th state is "no blob" detected, which is a fail state
# - reward state is the "middle", although this robot currently
#         has an offset camera, so might adjust that.
# ACTIONS (7)
# - range from hard left to hard right. "straight" is in the middle. 

class ServoingEnvironment:

    def __init__(self) -> None:

        self.vision = blob.PiBlob()

        # currently, actions are directions + time (ms) motor is on
        self.actions = [
            ["left",500], ["left", 300], ["left",150], ["fwd",150],
            ["right",500], ["right", 300], ["right",150] ]

        self.num_of_actions = len(self.actions)
        self.image_divisions = 11
        self.num_of_states = self.image_divisions + 1
        self.image_width = self.vision.image_width

        # signifies blob is not in the visual field
        self.no_blob = self.num_of_states - 1

        self.reward_state = (self.image_divisions)//2    # in the middle
        self.current_state = self.no_blob
        
        #vhandle = threading.Thread(target = visual.main)
        # vhandle.start()
        
    def reset(self):
        # Put the robot in a starting position.
        print("RVR being reset")
        #drive.drive(["right"],221)
        return self.get_state()

    def get_state(self):
        # Retrieve y-position of the blob
        #return random.randint(0,self.num_of_states)
        self.vision.capture()
        self.vision.find_blob()
       
        blob = self.vision.blob
        if len(blob)>0:
            state = int(blob[0][1]*self.image_divisions/480)
        else:
            state = self.no_blob
        return state
    
       # print(y_value, "This is being returned?")
        #width = 480
        #blob = pi.get_blob()
        #state =  (self.num_of_states / width) * y
        #self.current_state = blob[1]
        #return state

    # s1,r,d = env.step(a)
    def step(self,action):
        # Send action command to robot and get next state.
        driveParams = self.actions[action]
        print("DRIVING",driveParams[0],driveParams[1])
        input("return to continue ...")
        #drive.drive(driveParams[0], driveParams[1])
        
        #sleep(0.5)  # delay for 2 seconds to let it drive
        new_state = self.get_state()
        reward = 0
        done = False
        if (new_state == self.reward_state):
            reward = 1
            done = True    # reached goal. done
        elif (new_state == self.no_blob):
            reward = 0
            done = True    # failed. done.
        else:
            reward = 0
        return new_state, reward, done



