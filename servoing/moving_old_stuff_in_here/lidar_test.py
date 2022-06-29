# trying this from stack overflow
import sys
sys.path.append('python/')

from lidar_lite import Lidar_Lite


lidar = Lidar_Lite()
connected = lidar.connect(1)

if connected < -1:
    print ("Not Connected")
else:
    print("Connected")

while (connected > -1):
    print (lidar.getDistance())
    #print (lidar.getVelocity())