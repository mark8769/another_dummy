#!/usr/bin/python

# Standard imports
import sys
import cv2
import numpy as np
import importlib
# If you remove this it might stop checking for rover drivers being up to date
#import drive

sys.path.append('../')
blob_y_value = 0
window_name = "Win_Name"
point = (0,0)


def onmouse(event,x,y,flags,params):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        print (x,y)
        
def on_trackbar(val):
    hsv_low[0] = cv2.getTrackBarPos()

    
#put this line inside main setup, if anything breaks check here
#cv2.createTrackbar('H Low', window_name,0,255,dummy)
#read trackbar positions for all

#hul=cv2.getTrackbarPos('H Low', window_name)

'''
1. Converts source image to binary images by applying min-max Threshold
2. Extract connected components from every binary image by findContours and calculate their centers
3. Group centers from several binary images by their coordinates
4/ From the groups, estimate final centers of blobs and their radiuses and return as locations and sizes of keypoints
'''
def create_blob_detector():
    # create blob detector, then modify its params for detecting blobs
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 255

    # by colorimport importlib
    # changing to true 5/18/22
    '''
    Compares the intensity of a binary image at the center of a blob to blobcolor
    If they differ, the blob is filtered out
    blobColor = 0 to extract dark blobsq
    blobColor = 255 to extrack light blobs
    '''
    params.filterByColor = True
    # changed to true, so this would do something
    params.blobColor = 160
    
    '''
    Extracted blobs have an aread between minArea(inclusive)
    and maxArea(exclusive)
    '''
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 80000
    
    '''
    Extracted blobs have an area between minArea(inclusive)
    and between maxArea (exclusive) 4 * pi * Area / (perim * perim)
    '''
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.5
    #params.maxCircularity = something value
    
    '''
    Extracted blobs have convexity (area/area of blob convex hull) between
    minConvexity (inclusive) and maxConvexity(exclusive)
    '''
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.01
    #params.maxConvexity = something value
    
    '''
    Extracted blobs have this ratio between minInertiaRatio(inclusive)
    and maxInertialRation(exclusive)
    '''
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.1
        
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else : 
        detector = cv2.SimpleBlobDetector_create(params)

    return detector


def detect_object(image, res):
    
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("GRAY",res)
    cnts, hierarchy = cv2.findContours(res,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area = np.array([cv2.contourArea(k) for k in cnts])
    print("AREA",area)
    # gets values greater than 10 and less than 100,000
    cnts = np.array(cnts)[np.logical_and(area>10, area<100000)].tolist()
    area = area[np.logical_and(area>10, area<100000)]
    
    mask2 = np.zeros(res.shape)
    cv2.drawContours(mask2,cnts,-1,(255,255,255),-1)
    image_copy = np.copy(image)
    
    for cnt in np.arange(len(cnts)):
        rect = cv2.boundingRect(cnts[cnt])
        x,y,w,h = rect
        centre_x = int(x + (w / 2))
        centre_y = int(y + (h / 2))
        #print w,h
        cv2.rectangle(res,(centre_x-10,centre_y-10),(centre_x+10,centre_y+10),(255,0,0),2)
    
    # show Contours window
    cv2.imshow("CONTOURS", res)
    return image_copy, len(cnts)

def main():
    # Setup SimpleBlobDetector parameters.
    detector = create_blob_detector()

    # define HSV color thresholds
    hsv_low = np.array([152,169,98])
    hsv_high = np.array([179,255,255])
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name,onmouse)
    #creates a trackbar named 'H Low, attached to window_name window, trackbar has values from 0 - 255
    window_name_trackbar = "H Low"
    cv2.createTrackbar(window_name_trackbar, window_name,0,255,on_trackbar)

    # open video captureing
    cap = cv2.VideoCapture(-1)

    # capture, detect, display until quit signal
    capturing = True
    while capturing:
        # is_image_captured let us know if image is being captured
        # frame is video capture, or still image
        is_image_captured, frame = cap.read()
        # "im" changed to "frame_resized"
        frame_resized = cv2.resize(frame,(640,480))
        cv2.imshow("IMAGE",frame_resized)
        hsv_image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
        #cv2.imshow("HSV",hsv_image)
        
        cv2.setMouseCallback("IMAGE",onmouse)
        '''
        Pretty sure we dont need these here, keep for now
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name,onmouse)
        '''
        #cv2.getTrackbarPos(window_name_trackbar, window_name)
        mask = cv2.inRange(hsv_image,hsv_low, hsv_high)
        print(len(mask))
        cv2.imshow("MASK",mask)
        res = cv2.bitwise_and(frame_resized, frame_resized, mask = mask)
        res = cv2.bitwise_not(res)
        #cv2.imshow("MASKED IMAGE",hsv_image)
        image_copy,count = detect_object(frame_resized,hsv_image)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_copy,'frame %s Count %s' %(frame,count),(10,50), font, 1,(255,255,0),1)
        #cv2.imshow('Video',image_copy)

        keypointsC = detector.detect(hsv_image)
        print(len(keypointsC),keypointsC)

        # Draw detected blobs as red c ircles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(hsv_image, keypointsC, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        #Show blobs
        cv2.imshow("Keypoints Color", im_with_keypoints)
            
        #detect_object(im,mask)
        detect_object(im,hsv_image)
        
        # Detect blobs.
        keypoints = detector.detect(mask)

        # Draw detected blobs as red c ircles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        #Show blobs
        cv2.imshow("Keypoints", im_with_keypoints)
        key = cv2.waitKey(1)
        print("***************************",key)
        #alternatively, for 64 bit machines, not sure what the rasberry pi is running
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
        #ord() returns the number representing the unicode code of a specified character
        if key == ord('q'):
            print("***** pressed q*****")
            capturing = False
        # END WHILE LOOP capture, detect, display
    # released resources for camera
    cap.release()
    # destroys all of the highGui windows
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    main()
    
