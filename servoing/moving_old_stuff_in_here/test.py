import sys
import cv2
import numpy as np
import importlib

def main():

    # open video captureing
    cap = cv2.VideoCapture(-1)

    capturing = True
    
    while capturing:
        # is_image_captured let us know if image is being captured
        # frame is video capture, or still image
        is_image_captured, frame = cap.read()
        # "im" changed to "frame_resized"
        #frame_resized = cv2.resize(frame,(640,480))
        cv2.imshow("IMAGE",frame)

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