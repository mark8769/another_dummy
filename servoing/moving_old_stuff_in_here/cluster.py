class Cluster():
    def __init__(self, angle, angle_two, start, end, x_one, x_two, y_one, y_two):
        
        # TODO: Prob. dont need, save just in case
        self.start = start
        self.end = end
        # self.width = x2 - x1
        # start corresponds to x_one
        # end corresponds to x_two
        self.x_one = x_one
        self.x_two = x_two
        self.y_one = y_one
        self.y_two = y_two
        self.angle_one = angle
        self.angle_two = angle_two
        self.width = x_two - x_one
        self.middle = self.width / 2
    
    
    def get_start_index(self):
        return self.start
    def get_end_index(self):
        return self.end
    def get_start_angle(self):
        return self.angle_one
    def get_end_angle(self):
        return self.angle_two
    def print_cluster(self):
        print("Start Index: ", self.start)
        print("End Index: ", self.end)
        print("X2: ", self.x_two)
        print("X1: ", self.x_one)
        print("Y2: ", self.y_two)
        print("Y1: ", self.y_one)
        print("Width of Cluster: ", self.width)
        print("Middle of Cluster: ", self.middle)
