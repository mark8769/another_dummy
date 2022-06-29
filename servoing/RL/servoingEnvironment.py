import os, sys, asyncio, numpy as np, cv2 as cv, random
from obstacle_detection_implementation import get_lidar_points
import numpy
sys.path.append("../")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from sphero_sdk import SpheroRvrObserver, Colors, RvrStreamingServices
from videoGet import VideoGet
from obstacle_detection_implementation import get_servoing_stuff
from drive import driver, color_detected_handler
from detector import createDetector, blobDetector

class ServoingEnvironment:

    def __init__(self) -> None:
        
        # Creates RVR object
        self.rvr = SpheroRvrObserver()
        # Enables the rovers bottom facing color sensor
        self.rvr.enable_color_detection(is_enabled=True)
        # Creates the handler for the RVR's color detection
        self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.color_detection,
            handler=color_detected_handler
        )

        # Lists out actions that the rover can take.
        # NOTE: Legend: [rvrObject, L-trk drive mode, R-trk drive mode,.. 
        # ..drive time (seconds), speed, command name, led color code]
        # Drive Modes: 0 - Stop, 1 - Forward, 2 - Reverse
        self.actions = []
        self.actions.append([self.rvr, 1, 2, .15, 180, "Hard Right"])
        self.actions.append([self.rvr, 1, 2, .1, 180, "Right"])
        self.actions.append([self.rvr, 1, 2, .05, 180, "Soft Right"])
        #self.actions.alidar_points = numpy.empty([3, 37], dtype=object)ppend([self.rvr, 1, 1, .25, 180, "Forward"])
        #self.actions.append([self.rvr, 2, 2, .25, 180, "Reverse"])
        self.actions.append([self.rvr, 2, 1, .05, 180, "Soft Left"])
        self.actions.append([self.rvr, 2, 1, .1, 180, "Left"])
        self.actions.append([self.rvr, 2, 1, .15, 180, "Hard Left"])

        # Gets number of possible actions
        self.numActions = len(self.actions)
        # number of slices image is divided into
        self.image_divisions = 7
        # This would be about our 7 divisions
        # X could be somewhere in here
        # average x_state = (0 - 90: 0), (90 - 180: 1), (180 - 270: 2)
        #                   (270 - 360: 3), (360 - 450: 4), (450 - 540: 5)  
        #                   (540 - 630: 6)
        self.image_width = 630
        
        # Used for returning the blob width state, which estimates how close a blob is
        #self.blobSizeStateDict = {20:0, 40:1, 60:2, 80:3, 90:4, 999999:5}
        self.lidar_angle_dict = {30:0, 60:1, 85:2, 95:3, 120:4, 150:5, 180:6}
        # goal would be 6 inches, or about 20 cm (7.87 inches) accounting for error
        # I guess this is the "image divisions" for me
        self.lidar_distance_dict = {20:0, 40:1, 60:2, 80:3, 100:4, 120:5, 140:6}
        # Calculates total possible states, additional state is for no blob detected
        # self.numStates = (self.image_divisions * len(self.blobSizeStateDict)) + 1
        self.numStates = (self.image_divisions * len(self.lidar_angle_dict)) + 1
        
        # Signifies that blob left RVR's view, or if RVR moved out of bounds
        #? Wouldn't this be just self.numStates? Adding 1 in last line for no blob detected
        self.failState = self.numStates - 1

        # Gets middle slice of image divisions for reward state
        # Need odd number of states to keep slice in the middle
        self.reward_state = (((self.image_divisions)//2) * len(self.lidar_angle_dict)) + max(self.lidar_angle_dict.values())
        self.current_state = self.failState

        #self.lidar_points = numpy.empty([3, 37], dtype=object)

    def randomRestart(self):
        # Generates a random-ish drive command for restarting the test
        restartLeftTrack = random.randint(1,2)
        if restartLeftTrack == 1:
            restartRightTrack = 2
        else:
            restartRightTrack = 1
        restartDrive = [self.rvr, restartLeftTrack, restartRightTrack, 
        random.uniform(.1,.5), 180, "Restart", [255,0,255]]

        return restartDrive, restartLeftTrack, restartRightTrack
    
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
        Use width and distance as states, get these values from lidar
        """
        # Gets the measured distance, and respective angle from middle of object
        distance, angle = get_servoing_stuff()
        
        if distance is None:
            # we will just say its the furthest value in our dict
            distance = 110
        if angle is None:
            angle = 180

        # -90, 0, 90 is the way servo scans, all the way to left, middle, all the way to right
        if angle < 0:
            angle = abs(angle) + 90
        else:
            angle = angle - 90
        
        # Gets the state of the x-coordinate of the blob
        # I dont think we use distance here, use the angle to replicate whatever they're doing
        # My sliced would be the pi slices from a unit circle
        # So my "image width" would be 180 to get the index of whatever I have in the dict
        # this would be the index value for where object is located
        blobXLocationState = int(angle * self.image_divisions / 180)
        
        # pull dict items into a list of tuples, dict_items object
        lidar_entries = self.lidar_distance_dict.items()
        # dict_items list not subscriptable, cast to list
        lidar_entries = list(lidar_entries)
        #print(lidar_entries)
        
        print(distance)
        distance_bin_index = None
        temp_tuple = None
        
        for i in range (len(lidar_entries)):

            temp_tuple = lidar_entries[i]
            
            if distance < temp_tuple[0]:
                distance_bin = i
        if distance_bin is None:
            distance_bin = 6
        # Combines the blob x-coordinate state and blob size into a single state
        state = (blobXLocationState * len(self.lidar_distance_dict)) + distance_bin
        
        self.rvr.led_control.set_all_leds_rgb(red=255, green=165, blue=0)
        
        return state

    def step(self, action):
        # Send action command to robot and get next state.
        driveParams = self.actions[action]
        asyncio.run(driver(*driveParams))
        print(f"Driving: {driveParams[-1]}")
        print(f"Reward State: {self.reward_state}")
        new_state = self.get_state()

        reward = 0
        completeStatus = False

        if (new_state == self.reward_state):
            reward = 1
            completeStatus = True
            # reached goal. done, leds set to green
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
        return new_state, reward, completeStatus

