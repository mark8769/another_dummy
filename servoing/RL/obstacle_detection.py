'''
Mark Ortega-Ponce
Created - 6/x/22
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

# pass an array of values? Make array of tuples?
# this is to filter out noise, not necessary to work
# try implementing after?
def median_filtering(lidar_points):

    '''
    Only modifying the second row
    Lidar points contains 3 rows of lidar points
    All are the same scans, some contain noise, some dont
    Never modify first row because we'll get out of bounds
    Similar with last row.
    '''
    
    average = 0
    sum = 0

    filtered_points = numpy.empty([1, len(lidar_points[0])], dtype=object)
    # grab first and last values as we wont be modifying them at all
    filtered_points[0][0] = lidar_points[1][0]
    filtered_points[0][len(lidar_points[0]) - 1] = lidar_points[1][len(lidar_points[0]) - 1]
    
    for t in range (1, len(lidar_points) - 1):
        # want to look at previous, current, next_point
        # start index at 1, end 1 before last
        # prevent out of bounds for both start and end
        sum = 0
        for i in range (1, len(lidar_points[0]) - 1):

            first = lidar_points[t - 1][i - 1].get_distance()
            second = lidar_points[t - 1][i].get_distance()
            third = lidar_points[t - 1][i].get_distance()
            fourth = lidar_points[t][i - 1].get_distance()
            fifth = lidar_points[t][i].get_distance()
            sixth = lidar_points[t][i + 1].get_distance()
            seventh = lidar_points[t + 1][i - 1].get_distance()
            eight = lidar_points[t + 1][i].get_distance()
            ninth = lidar_points[t + 1][i + 1].get_distance()

            sum = first + second + third + fourth
            sum += fifth + sixth + seventh + eight + ninth
            # float division first, then round down
            average = int(sum / 9)

            lidar_points[t][i].set_distance(average)
            filtered_points[t - 1][i] = lidar_points[t][i]

            #visualize_points(lidar_points)

    # return single row filtered list, and ignore other 2 scans?
    return filtered_points, lidar_points


def satifies_equations(lidar_point_list):
                
    for i in range (len(lidar_point_list)):
        for j in range (len(lidar_point_list[0])):
            if lidar_point_list[i][j].get_has_index():
                lidar_point_list[i][j].print_obstacle_range()
                print("Passed Start Equation: ", satifies_start_equation(lidar_point_list, i, j))
                print("Passed End Equation: ", satifies_end_equation(lidar_point_list, i, j))
            
def satifies_start_equation(lidar_point_list, row, col):
    
    index = lidar_point_list[row][col].get_start_wall_index()
    
    previous_point = index - 1
    current_point = index
    
    if not lidar_point_list[row][previous_point].is_obstacle() and lidar_point_list[row][current_point].is_obstacle():
        return True
    else:
        return False
    
def satifies_end_equation(lidar_point_list, row, col):
    
    index = lidar_point_list[row][col].get_end_wall_index()
    current_point = index
    next_point = index + 1

    if lidar_point_list[row][current_point].is_obstacle() and not lidar_point_list[row][next_point].is_obstacle():
        return True
    else:
        return False
    
    
def prep_filtered(point_list):
    
    for i in range(len(point_list)):
        for j in range(len(point_list[0])):
            if point_list[i][j].get_distance() < 80:
                point_list[i][j].set_is_obstacle(True)
            else:
                point_list[i][j].set_is_obstacle(False)
                
    return point_list

def preprocessing_laser_point(point_list):

    start_index = 0
    
    for i in range(len(point_list)):
        # our threshold for is_obstacle is if distance is less than 40
        # this is for start[i] section in paper
        for j in range(1, len(point_list[0])):
            if not point_list[i][j - 1].is_obstacle() and point_list[i][j].is_obstacle():
                point_list[i][j].set_start_wall_index(j)
                start_index = j
            if point_list[i][j].is_obstacle() and not point_list[i][j + 1].is_obstacle():
                point_list[i][start_index].set_end_wall_index(j)
                
    return point_list
            
def prepocessing_separation(point_list):
    #for i in range(1, len(point_list)):
    pass

def print_all_points(lidar_points):

    print()
    print("Row size: ",len(lidar_points))
    print("Column size: ", len(lidar_points[0]))
    print("TESTING---------------------------------------------")
    for i in range(len(lidar_points)):
        for j in range(len(lidar_points[0])):
            lidar_points[i][j].print_point()

def visualize_points(lidar_points):
    #print column numbers to visualize the data
    for i in range(1):
        for j in range(len(lidar_points[0])):
            if lidar_points[i][j].get_angle() == 90:
                print(j, end="  ")
            else:
                print(j, end=" ")
    
    print()
    print("----------------------------------------------------------------------------------------------------")
    string = " "
    for i in range(len(lidar_points)):
        if i != 0:
            print()
        string = " "
        for j in range(len(lidar_points[0])):
            if j > 9:
                string = "  "
            if lidar_points[i][j].is_obstacle():
                print("-", end=string)
            else:
                print("0", end=string)
    print()

def add_clusters(lidar_points):

    cluster_list = []
    temp_start = None
    temp_end = None
    x_two = None
    y_one = None
    x_one = None
    y_two = None
    distance = None
    angle = None
    angle_two = None
    
    for i in range(len(lidar_points)):
        for j in range(len(lidar_points[0])):
            if lidar_points[i][j].get_has_index():
                temp_start = lidar_points[i][j].get_start_wall_index()
                temp_end = lidar_points[i][j].get_end_wall_index()
                x_one = lidar_points[i][temp_start].get_x()
                x_two = lidar_points[i][temp_end].get_x()
                y_one = lidar_points[i][temp_start].get_y()
                y_two = lidar_points[i][temp_end].get_y()
                angle = lidar_points[i][temp_start].get_angle()
                angle_two = lidar_points[i][temp_start].get_angle()
                dist_one = lidar_points[i][temp_start].get_distance()
                dist_two = lidar_points[i][temp_end].get_distance()
                cluster = Cluster(angle, angle_two, temp_start, temp_end, x_one, x_two, y_one, y_two, dist_one, dist_two)
                cluster_list.append(cluster)

    #print(len(cluster_list))
    #print(cluster_list)

    return cluster_list
