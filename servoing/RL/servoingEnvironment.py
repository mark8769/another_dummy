import asyncio
import os
import random
import sys
import time
import warnings
sys.path.append("../")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from sphero_sdk import SpheroRvrObserver, Colors, RvrStreamingServices
from videoGet import VideoGet
from obs_two_pass import get_servoing_stuff as get_servoing_two
from obs_three_pass import get_servoing_stuff as get_servoing_three
from drive import driver, color_detected_handler
from simulated_scan import get_dummy_data

class ServoingEnvironment:

    def __init__(self) -> None:
        

        # Creates RVR (Observer) object
        self.rvr = SpheroRvrObserver()
        
        # Enables the rovers bottom facing color sensor
        self.rvr.enable_color_detection(is_enabled=True)
        
        # Creates the handler for the RVR's color detection
        self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.color_detection,
            handler=color_detected_handler
        )

        # Creates flag for when RVR detects a specific color with it's sensor
        self.colorFlag = True

        # Lists out actions that the rover can take.
        # NOTE: [rvrObject, L-trk drive mode, R-trk drive mode,.. 
        # ..drive time (seconds), speed, command name, led color code]
        # Drive Modes: 0: Stop, 1: Forward, 2: Reverse
        #[self.rvr, 1, 1, .4, 160, "Fast Forward"],
        #[self.rvr, 1, 1, .2, 160, "Forward"],
        #[self.rvr, 1, 1, .1, 160, "Slow Forward"],
        self.actions = [
            [self.rvr, 1, 2, .15, 180, "Hard Right"],
            [self.rvr, 1, 2, .1, 180, "Right"],
            [self.rvr, 1, 2, .05, 180, "Soft Right"],
            [self.rvr, 2, 1, .05, 180, "Soft Left"],
            [self.rvr, 2, 1, .1, 180, "Left"],
            [self.rvr, 2, 1, .15, 180, "Hard Left"]
        ]
        
        # Unused but valid actions:
        # [self.rvr, 2, 2, .25, 180, "Reverse"]


        # Gets number of possible actions by measuring actions list length
        self.numActions = len(self.actions)
        
        # Sets the number of vertical bins the frame is sliced into
        # Curr for lidar = 7 also, the pi slices.
        # This would be about our 7 divisions
        # X could be somewhere in here
        # average x_state = (0 - 90: 0), (90 - 180: 1), (180 - 270: 2)
        #                   (270 - 360: 3), (360 - 450: 4), (450 - 540: 5)  
        #                   (540 - 630: 6)
        
        # This is used to decide which sonar distance state the RVR in
        #self.distanceStateDict = [[240,0], [160, 1], [80,2], [20,3], [5,4], [0,5]]
        self.lidar_angle_dict = {30:0, 60:1, 80:2, 100:3, 120:4, 150:5, 180:6}
        self.image_divisions = len(self.lidar_angle_dict)
        #self.lidar_distance_dict = {20:0, 40:1, 60:2, 80:3, 100:4, 120:5, 140:6}
        self.lidar_distance_dict = {50:0, 60:1, 80:2, 100:3, 120:4, 140:5, 160:6}
        # Sets number of possible states, added state is for no blob detected
        self.numStates = (self.image_divisions * len(self.lidar_distance_dict)) + 1

        # numStates = 7 * 7 + 1 = 50
        # Signifies that blob left RVR's view, or if RVR moved out of bounds, 49th state
        self.failState = self.numStates - 1

        # Gets middle slice of image divisions for reward state
        # 7 // 2 --> 3 * 7 + (max value of dict values, mine would be 180)
        # 21 + (index not angle) 6 = 27 ~ middle slice would be 
        self.reward_state = (((self.image_divisions)//2) * len(self.lidar_angle_dict)) + max(self.lidar_angle_dict.values())
        
        self.current_state = self.failState

    def randomRestart(self):
        # Generates a random-ish drive command for restarting the test
        restartLeftTrack = random.randint(1,2)
        if restartLeftTrack == 1:
            restartRightTrack = 2
        else:
            restartRightTrack = 1
        restartDriveCommand = [self.rvr, restartLeftTrack, restartRightTrack, 
        random.uniform(.1,.5), 180, "Restart", [255,0,255]]

        return restartDriveCommand, restartLeftTrack, restartRightTrack

    def reset(self):
        """This has the RVR place itself into a somewhat-random starting position by rotating"""
        print("RVR being reset")
        state = self.failState
        restartDriveCommand, restartLeftTrack, restartRightTrack = self.randomRestart()
        asyncio.run(driver(*restartDriveCommand))
        
        # The RVR will rotate until it sees a blob. (Search mode)
        while state == self.failState:
            # move first, then get_state
            asyncio.run(driver(*[self.rvr, restartLeftTrack, restartRightTrack, .2, 180, "Scanning"]))
            # I am assuming get my width and midpoint here, instead of blob
            state = self.get_state()

        return state
    
    def get_state(self):
        """
        Gets a video frame, searches for blobs in the frame using the detector.
        """
        # Gets the measured distance, and respective angle from middle of object
        distance, angle = get_servoing_two()
        #distance, angle = get_servoing_three()

        # if no obstacle found then fail
        if distance is None or angle is None:
            state = self.failState
            return state
        
        # Gets the state of the x-coordinate of the blob
        # I dont think we use distance here, use the angle to replicate whatever they're doing
        # My sliced would be the pi slices from a unit circle
        # So my "image width" would be 180 to get the index of whatever I have in the dict
        # this would be the index value for where object is located
        #blobXLocationState = int(angle * self.image_divisions / 180) ;;TODO: Check on Tuesday

        # pull dict items into a list of tuples, dict_items object
        # dict_items list not subscriptable, cast to list
        angle_entries = self.lidar_angle_dict.items()
        angle_entries = list(angle_entries)
        angle_bin_index = None
        
        for tup in angle_entries:
            if angle < tup[0]:
                angle_bin_index = tup[1]
                break  
        if angle_bin_index is None:
            angle_bin_index = len(self.lidar_angle_dict) - 1
        
        blobXLocationState = angle_bin_index
        
        lidar_entries = self.lidar_distance_dict.items()
        lidar_entries = list(lidar_entries)
        distance_bin_index = None
        
        for tup in lidar_entries:
            if distance < tup[0]:
                distance_bin_index = tup[1]
                break
                
        if distance_bin_index is None:
            distance_bin_index = len(self.lidar_distance_dict) - 1
    
        # Combines the blob x-coordinate state and blob size into a single state
        state = (blobXLocationState * len(self.lidar_distance_dict)) + 6
        # I think this line is somehow messing up the drive commands.
        #+ distance_bin_index
        print(f"xLocState: {blobXLocationState}, Distance: {distance_bin_index}, Combined State: {state}")
        self.rvr.led_control.set_all_leds_rgb(red=255, green=165, blue=0)
        return state

    def step(self, action):
        # Send action command to robot and get next state.
        driveParams = self.actions[action]
        self.colorFlag = asyncio.run(driver(*driveParams))
        print(f"Color Flag: {self.colorFlag}")
        print(f"Driving: {driveParams[-1]}")
        print(f"Reward State: {self.reward_state}")
        new_state = self.get_state()
        
        # Resets the colorFlag after setting the state

        reward = 0
        completeStatus = False
        # Debugging: print(f"Before if/else in Step(): New State: {new_state}, Reward: {reward}, Complete Status {completeStatus}")
        if (new_state == self.reward_state):
            reward = 1
            completeStatus = True
            # reached goal. done, leds set to green
            self.colorFlag = True
            self.rvr.led_control.set_all_leds_rgb(red=0, green=255, blue=0)
        elif (new_state == self.failState):
            reward = 0
            completeStatus = True
            # failed. done, leds set to red
            self.rvr.led_control.set_all_leds_rgb(red=255, green=0, blue=0)
        else:
            reward = 0
            # Not done, still searching, leds set to orange
            self.rvr.led_control.set_all_leds_rgb(red=255, green=165, blue=0)
        # Debugging: print(f"End of Step(): New State: {new_state}, Reward: {reward}, Complete Status {completeStatus}")
        return new_state, reward, completeStatus
