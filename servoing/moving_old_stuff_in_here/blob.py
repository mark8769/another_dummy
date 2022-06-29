#!/usr/bin/python

# Standard imports
import sys
import cv2
import subprocess
import numpy as np

show_images = True

class PiBlob:

    def __init__(self):

        # blob is [ [x,y], size ]
        self.blob = [ [-1,-1], -1]

        self.im = None

        self.image_width = 480
        self.image_height = 270
        
        # search for blobs that fall in this color range]
        self.low_color = np.array([155,50,250])
        self.high_color = np.array([185,255,255])

        # create the blob detector
        self.params = cv2.SimpleBlobDetector_Params()
        self.set_detector_params()
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
            self.detector = cv2.SimpleBlobDetector(self.params)
        else : 
            self.detector = cv2.SimpleBlobDetector_create(self.params)

        #self.cap = cv2.VideoCapture(0)


    def set_detector_params(self):
        # Setup SimpleBlobDetector parameters.
    
        # Change thresholds
        self.params.minThreshold = 0
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 10
        self.params.maxArea = 80000

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5

        # Filter by Convexity
        self.params.filterByConvexity = False
        self.params.minConvexity = 0.01
            
        # Filter by Inertia
        self.params.filterByInertia = False
        self.params.minInertiaRatio = 0.1
        
    def capture(self):
        subprocess.run(["raspistill","--nopreview","-o","image.jpg"])
        #with picamera.PiCamera() as camera:
            #camera.resolution = (480,270)
            #camera.start_preview()
            #time.sleep(2)
            #camera.capture('image.jpg', 'bgr')

    def find_blob(self):

        # okay, probably not the most efficient means
        # to "stream" images, but we will live with it for now.
        self.im = cv2.imread("image.jpg");
        self.im = cv2.resize(self.im,(self.image_width,self.image_height))

        # Convert to hsv (not sure why blob detection is hsv,
        # but that is what all the examples show)
        hsv_im = cv2.cvtColor(self.im,cv2.COLOR_BGR2HSV)
        
        # Mask image using color ranges and convert to
        # black blobs on white background
        masked_im = cv2.inRange(hsv_im, self.low_color, self.high_color)
        masked_im = cv2.bitwise_not(masked_im)

        # Detect blobs.
        keypoints = self.detector.detect(masked_im)

        print("KEYPOINTS (",len(keypoints),"):",keypoints)

        # need to fix this so if blob not detected, returns fail state
        # also need to fix this to check for multiple blobs
        if len(keypoints)>0:
            self.blob = [ keypoints[0].pt, 0 ]
        else:
            self.blob = []
            
        if (show_images):
            im_with_keypoints = cv2.drawKeypoints(masked_im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv2.imshow("Keypoints", im_with_keypoints)

    
