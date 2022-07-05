'''
obstacle_detection.py

Created - Mark Ortega-Ponce

Purpose: To find obstacles from 
        scanning our lidar in a 180 degree view.
        Goal is to move towards objects found, so
        contradictory to filename. Obstacle
        avoidance parts in paper have been ignored
        for now.

Source: https://www.researchgate.net/publication/308818311_The_obstacle_detection_and_obstacle_avoidance_algorithm_based_on_2-D_lidar
Download link on the website
'''
import math
import numpy
from point import Point
from cluster import Cluster

def position_laser_point(angle_i, distance):
    # converting angle to radians for math.cos() function
    # if we get a -90 means we want to subtract 90
    # take the abs and get back 180 to follow the degrees in a unit circle
    angle_i = angle_i - 90
    angle_i = abs(angle_i)

    angle_in_radians = math.radians(angle_i)
    # not completely sure if I need the - 5 part
    # paper has their range from -5 to +185, I think thats where they get the - 5
    # in the paper they have i is in the set of 0 - 190, so thats why they have -5
    # removing for right now, note it anyway
    point_xi = distance * math.cos(angle_in_radians)
    point_yi = distance * math.sin(angle_in_radians)
    
    return point_xi, point_yi

def position_laser_point_pan_tilt(angle_i, tilt_angle, distance):

    angle_i = angle_i - 90
    angle_i = abs(angle_i)

    # Math.sin/cos functions take angles in radians.
    angle_in_radians = math.radians(angle_i)
    tilt_angle_in_radians = math.radians(tilt_angle)

    '''
    Xi = Ri * cos(i) * cos(alpha)
    Yi = Ri * sin(i) * cos(alpha)
    Paper range: i in the set of (0, 190) or (-5, 185, actual angles being used)
    Our range: i in the set of (0, 180) or (0, 180) so we exclude the -5 they use.
    '''
    point_xi = distance * math.cos(angle_in_radians) * math.cos(tilt_angle_in_radians)
    point_yi = distance * math.sin(angle_in_radians) * math.cos(tilt_angle_in_radians)    

def median_filtering(lidar_points):
    '''
    Filter out noise in the sweeps.
    We do three sweeps, starting from -90: 90, 90: -90, -90: 90
    We average the middle sweep with surrounding values
    to filter out any noise.
    '''    
    average = 0
    sum = 0

    # Create a single row list, same column size as lidar_points
    filtered_points = numpy.empty([1, len(lidar_points[0])], dtype=object)
    # grab first and last points as we won't be able to modify them
    # with the way the paper did it
    filtered_points[0][0] = lidar_points[1][0]
    filtered_points[0][len(lidar_points[0]) - 1] = lidar_points[1][len(lidar_points[0]) - 1]
    
    # Iterate over rows starting at 1, ending one before last value
    for t in range (1, len(lidar_points) - 1):
        # want to look at previous, current, next_point
        # start index at 1, end 1 before last
        # prevent out of bounds for both start and end
        sum = 0
        for i in range (1, len(lidar_points[0]) - 1):
            # Grabbing first sweep values
            # Point prev, point curr, point next
            first = lidar_points[t - 1][i - 1].get_distance()
            second = lidar_points[t - 1][i].get_distance()
            third = lidar_points[t - 1][i].get_distance()
            # Grabbing second sweep values
            # Point prev, point curr, point next
            fourth = lidar_points[t][i - 1].get_distance()
            fifth = lidar_points[t][i].get_distance()
            sixth = lidar_points[t][i + 1].get_distance()
            # Grabbing third sweep values
            # Point prev, point curr, point next
            seventh = lidar_points[t + 1][i - 1].get_distance()
            eight = lidar_points[t + 1][i].get_distance()
            ninth = lidar_points[t + 1][i + 1].get_distance()

            # Add all points we gathered from above
            sum = first + second + third + fourth
            sum += fifth + sixth + seventh + eight + ninth
            # float division first, then round down
            average = int(sum / 9)
            # Assign new distance value which is the average
            # of all the points adjacent to it.
            # Eg. top/bottom, adjacent left/right, diagonal corners
            # Eg. A cube {0, 0, 0       {0, x, x, x, 0  Move to next column, repeat.
            #             0, M, 0   -->  0, x, M, x, 0
            #             0, 0, 0}       0, x, x, x, 0}
            # Modifying M only, which is current point being iterated over.
            lidar_points[t][i].set_distance(average)
            filtered_points[t - 1][i] = lidar_points[t][i]

    # return single list because thats all we care about
    # return single row filtered list, return original list
    return filtered_points, lidar_points

def median_filtering_two_pass(lidar_points):
    '''
    Median filtering for only two passes.
    3 passes found to be too slow in the RL environment.
    Filter out noise in the sweeps.
    Sweep from -90 to 90.
    Sweep from 90 back to -90.
    Start over again.
    '''    
    average = 0
    sum = 0

    filtered_points = numpy.empty([1, len(lidar_points[0])], dtype=object)
    # grab first and last values as we wont be modifying them at all
    filtered_points[0][0] = lidar_points[1][0]
    filtered_points[0][len(lidar_points[0]) - 1] = lidar_points[1][len(lidar_points[0]) - 1]
    
    for t in range (1, 2):
        for i in range(1, len(lidar_points[0]) - 1):

            first = lidar_points[t - 1][i - 1].get_distance()
            second = lidar_points[t - 1][i].get_distance()
            third = lidar_points[t - 1][i].get_distance()
            fourth = lidar_points[t][i - 1].get_distance()
            fifth = lidar_points[t][i].get_distance()
            sixth = lidar_points[t][i + 1].get_distance()
            
            sum = first + second + third + fourth + fifth + sixth
            average = int(sum / 6)
            
            lidar_points[t][i].set_distance(average)
            filtered_points[t - 1][i] = lidar_points[t][i]
            
    return filtered_points, lidar_points

'''
This function checks the lidar point cloud data.
It follows the formulas for finding start_index and end_index values
found in the paper. If a point is found to have a start index
we keep a temp value with the current index where start was found.
Once we find a point that IS not an obstacle, we update the end_index value
of where we first found the starting point of our obstacle.
'''
# Password for new wifi: steinmetz
def preprocessing_laser_point(point_list):

    start_index = 0
    edge_case = False
    one_time_flag = False
    
    for i in range(len(point_list)):
        for j in range(1, len(point_list[0]) - 1):
            
            if point_list[i][0].is_obstacle() and not one_time_flag:
                start_index = 0
                point_list[i][start_index].set_start_wall_index(start_index)
                edge_case = True
                one_time_flag = True
            
            # 
            if edge_case and not point_list[i][j - 1].is_obstacle():
                point_list[i][start_index].set_end_wall_index(j - 2)
                edge_case = False
                
            if not point_list[i][j - 1].is_obstacle() and point_list[i][j].is_obstacle() and not edge_case:
                # set as start of new wall
                point_list[i][j].set_start_wall_index(j)
                start_index = j
                    
            if point_list[i][j].is_obstacle() and not point_list[i][j + 1].is_obstacle() and not edge_case:

                point_list[i][start_index].set_end_wall_index(j)
                
            # if we are one before end of list, and we have an obstacle
            # just say last point is the end of obstacle since we can't scan further
            if j == (len(point_list[0]) - 2) and point_list[i][start_index].get_end_wall_index() == -1:
            
                point_list[i][start_index].set_end_wall_index(len(point_list[0]) - 1)
        
    return point_list

# TODO: Not really needed, this is for obstacle avoidance.
def prepocessing_separation(point_list):
    #for i in range(1, len(point_list)):
    pass

def add_clusters(lidar_points):

    cluster_list = []
    temp_start = None
    temp_end = None
    
    for i in range(len(lidar_points)):
        for j in range(len(lidar_points[0])):
            
            if lidar_points[i][j].get_has_index():
                
                temp_start = lidar_points[i][j].get_start_wall_index()
                temp_end = lidar_points[i][j].get_end_wall_index()
 
                cluster = Cluster(temp_start, temp_end, lidar_points)
                cluster_list.append(cluster)

    return cluster_list

                
                