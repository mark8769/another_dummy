from gpiozero import Servo
import math
import copy
import numpy
from time import sleep
import sys
from point import Point
from obstacle_detection import (
    position_laser_point,
    satifies_equations,
    preprocessing_laser_point,
    print_all_points,
    visualize_points,
    add_clusters,
    median_filtering,
    prep_filtered
)
from gpiozero.pins.pigpio import PiGPIOFactory
# get lidar_lite file from python folder
sys.path.append('python/')
from lidar_lite import Lidar_Lite
# set up PiGPIOFactory to use hardware and not software pwm
factory = PiGPIOFactory()
# set up servo, GPIO pin 12, min_pulse = .45ms, max_pulse = 2.45ms, use hardware
# https://hitecrcd.com/files/Servomanual.pdf
hitec_servo = Servo(12, min_pulse_width=.45/1000, max_pulse_width=2.45/1000, pin_factory=factory)
# set up lidar lite
lidar = Lidar_Lite()
# check if lidar is connected
connected = lidar.connect(1)

if connected < -1:
    print ("Not Connected")
else:
    print("Connected")
   
def set_servo_angle(angle, servo):
    # we have -1 to 1
    # we have range of (0, 2)
    # servo range is from (0, 180)
    # if we do 2 / 180
    # we have 0.01111111111111
    value = angle * 0.01111
    #print(angle)
    #print(value)
    if value < -1:
        value = -1
    
    if value > 1:
        value = 1
        
    servo.value = value

def get_lidar_points():

    angle_counter = -90
    degree_of_accuracy = 5
    angle_helper = degree_of_accuracy
    lidar_distance = None
    lidar_points = []
    # one sweep is 37 points when using 5 degrees of accuracy
    # range from (-90 to 90)
    lidar_points = numpy.empty([3, 37], dtype=object)
    #row, col = 3, 37
    #lidar_points = [[0] * col] * row
    row_counter = 0
    column_counter = 0
    column_helper = 1
    regular_counter = 1
    third_pass = False
    error_counter = 0

    while True:
        # servo goes from (-90, 90)
        # if we get past 90 want to sweep back
        if angle_counter > 90:

            angle_counter = 90
            angle_helper = -(degree_of_accuracy)
            column_helper = -1
            column_counter = 36
            row_counter += 1
            # break on third sweep
            if third_pass:
                break
        # if we get past -90 want to sweep back
        if angle_counter < -90:
            angle_counter = -90
            angle_helper = degree_of_accuracy
            column_helper = 1
            column_counter = 0
            row_counter += 1
            # complete one sweep to left, then right.
            # Set to true, to break on third pass
            third_pass = True
        
        set_servo_angle(angle_counter, hitec_servo)
        sleep(0.06)
        lidar_distance = lidar.getDistance()
        
        # if we get a bad reading, want to do take reading again
        # keep getting readings until we dont get -1
        # Edit: apparently after an error, we get about 10-15 bad readings
        # needed to modify this to account for this error
        # else only most inner whil0  0  0  -  -  -  -  -  -  -  -  e loop needed
        # if you're confused, lower the first while loop to 1 - 5 insteaf of 20
        if lidar_distance == -1:
            
            while error_counter < 20:
            
                lidar_distance = lidar.getDistance()
                error_counter += 1
            
                while lidar_distance == -1:
                    # reset error_counter
                    # after an error we get about 10-15 bad measurements
                    error_counter = 0
                    lidar_distance = lidar.getDistance()
        
        error_counter = 0
        x, y = position_laser_point(angle_counter, lidar_distance)
        point = Point(x,y, lidar_distance, angle_counter)
        #point.print_point()
        lidar_points[row_counter][column_counter] = point
        angle_counter += angle_helper
        column_counter += column_helper
    
    return lidar_points

def run_tests():

    lidar_points = numpy.empty([3, 37], dtype=object)
    lidar_points = get_lidar_points()
    # dont want to set obstacle for filtered points, so use this when creating filtered
    # make a copy, dont want to alias existing list
    # deepcopy if list contains objects
    temp_lidar_points = copy.deepcopy(lidar_points)
    lidar_points = preprocessing_laser_point(lidar_points)
    satifies_equations(lidar_points)
    print()
    print("BEFORE FILTERING")
    print("----------------------------------------")
    visualize_points(lidar_points)
    
    filtered_points = numpy.empty([1, len(lidar_points[0])], dtype=object)
    _, lidar_points = median_filtering(lidar_points)
    filtered_points, temp_lidar_points = median_filtering(temp_lidar_points)
    
    print()
    print("AFTER FILTERING")
    print("----------------------------------------")
    visualize_points(lidar_points)
    print()
    # [start, end, start, end ......]
    filtered_points = preprocessing_laser_point(filtered_points)

    print("VISUALIZING THE FILTERED POINT LIST")
    visualize_points(filtered_points)
    cluster_list = add_clusters(filtered_points)
    
    print()
    print("Checking cluster indexes")
    
    for cluster in cluster_list:
        print("Checking results with filtered list")
        print("-------------------------------------------------")
        print("Filtered list x1: ", filtered_points[0][cluster.get_start_index()].get_x())
        print("Filtered list x2: ", filtered_points[0][cluster.get_end_index()].get_x())
        cluster.print_cluster()
        
        
def get_servoing_stuff():

    lidar_points = numpy.empty([3, 37], dtype=object)
    filtered_points = numpy.empty([1, len(lidar_points[0])], dtype=object)
    
    lidar_points = get_lidar_points()
    filtered_points, _ = median_filtering(lidar_points)
    
    filtered_points = preprocessing_laser_point(filtered_points)
    cluster_list = add_clusters(filtered_points)
    
    visualize_points(filtered_points)
    temp_max = 0
    temp_cluster = None
    for cluster in cluster_list:
        
        temp_range = cluster.get_end_index() - cluster.get_start_index()
        
        if temp_range >= temp_max:
            
            temp_max = temp_range
            temp_cluster = cluster

    if temp_cluster is None:
        return 0
    else:
        temp_cluster.print_cluster()
    
    if temp_cluster == None:
        return -1, -1
    
    start_index = temp_cluster.get_start_index()
    end_index = temp_cluster.get_end_index()

    index_range = end_index - start_index
    index_range = index_range // 2
    
    index_to_access = start_index + index_range
    
    for i in range(len(filtered_points)):
        for j in range(start_index, end_index + 1):
            filtered_points[i][j].print_point()
    
    distance = filtered_points[0][index_to_access].get_distance()    
    angle = filtered_points[0][index_to_access].get_angle()
    
    print(angle)
    if angle <= 0:
        angle = abs(angle) + 90
    else:
        angle = abs(angle - 90)
    
    # return the distance of the middle point in the cluster
    # return the angle of the middle point in the cluster
    
    return distance, angle

def main():

    #run_tests()
    #run_tests()
    distance, angle = get_servoing_stuff()
    print("Distance Acquired: ", distance)
    print("Angle Acquired: ", angle)
    distance, angle = get_servoing_stuff()
    print("Distance Acquired: ", distance)
    print("Angle Acquired: ", angle)
    
if __name__ == '__main__':
    main()