'''
obstacle_detection_helper.py

Created - Mark Ortega-Ponce

Purpose: Helper functions for obstacle detection
        Visualize cloud point data gathered from servoing.
        Test to see if start_index and end_index are being
        recorded correctly.
'''

'''
Function to visualize cloud point data gathered.
'''
def visualize_points(lidar_points):
    
    # Print column numbers only.
    for i in range(1):
        # Iterate over the row count
        for j in range(len(lidar_points[0])):
            # print on same line
            # modify end of print to be space instead of newlines
            print(j, end=' ')
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
            elif lidar_points[i][j].is_wall():
                print("X", end=string)
            else:
                print("0", end=string)
    print()

'''
Function to print all points inside a lidar point cloud data list.
Point info consists of x, y, angle, distance.
Is the point an obstacle, and so on. 
'''
def print_all_points(lidar_points):

    print()
    print("Row size: ",len(lidar_points))
    print("Column size: ", len(lidar_points[0]))
    print("TESTING---------------------------------------------")
    for i in range(len(lidar_points)):
        for j in range(len(lidar_points[0])):
            lidar_points[i][j].print_point()

'''
Test shown in paper. Tests whether start_index
and end_index are valid values.
The start of an obstacle is when the previous point
was considered nothing important (like a wall)
and next point ended up being an obstacle.
A valid end_index value is when current point is
an obstacle, and next point is something like a wall.
'''
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

    