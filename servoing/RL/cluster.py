'''
cluster.py

Created - Mark Ortega-Ponce

Purpose: To store relevant information about obstacles found.
        We store start_index to access it in the filtered list.
        Note: I might just want to keep a list of points
        from start_index to end_index. But this was a quick class
'''
class Cluster():
    # Keep a reference of start/end and reference to list
    def __init__(self, start, end, filtered_points):
        
        self.start = start
        self.end = end
        self.index_range = (self.end - self.start) // 2
        self.center = self.start + self.index_range
        self.x_one = filtered_points[0][self.start].get_x()
        self.x_two = filtered_points[0][self.end].get_x()
        self.y_one = filtered_points[0][self.start].get_y()
        self.y_two = filtered_points[0][self.end].get_y()
        self.angle_one = filtered_points[0][self.start].get_angle()
        self.angle_two = filtered_points[0][self.end].get_angle()
        self.center_angle = filtered_points[0][self.center].get_angle()
        self.width = self.x_two - self.x_one
        self.middle = self.width / 2
        self.dist_one = filtered_points[0][self.start].get_distance()
        self.dist_two = filtered_points[0][self.end].get_distance()
        self.center_distance = filtered_points[0][self.center].get_distance()
    
    def get_start_index(self):
        return self.start
    def get_end_index(self):
        return self.end
    def get_center_index(self):
        return self.center
    def get_start_angle(self):
        return self.angle_one
    def get_center_angle(self):
        return self.center_angle
    def get_end_angle(self):
        return self.angle_two
    def get_center_distance(self):
        return self.center_distance
    def get_width(self):
        return self.width
    def get_middle(self):
        return self.middle
    def print_cluster(self):
        print("Start Index: ", self.start)
        print("End Index: ", self.end)
        print("X2: ", self.x_two)
        print("X1: ", self.x_one)
        print("Y2: ", self.y_two)
        print("Y1: ", self.y_one)
        print("Width of Cluster: ", self.width)
        print("Middle of Cluster: ", self.middle)
        print("Center angle: ", self.center_angle)
        print("Center distance: ", self.center_distance)
        print()
