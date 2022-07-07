'''
Point.py

Created - Mark Ortega-Ponce

6/x/22

Purpose: Store lidar point cloud data 
        from scanning an environment.
'''
class Point():
    
    # previously 200 cm
    obstacle_threshold = 200
    
    def __init__(self, x, y, distance, angle):
      
      self.x = x
      self.y = y
      self.distance = distance
      self.angle = angle
      
      self.start_w_index = None
      self.end_w_index = None
      self.wall = False
      self.has_wall_index = False
      
      self.start_wall_index = None
      self.end_wall_index = None
      self.has_index = False
      # for preprocessing of laser point cloud data
      # part B in paper
      if distance <= Point.obstacle_threshold:
          self.obstacle = True
      else:
          self.obstacle = False
          self.wall = True
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_angle(self):
        return self.angle
    def get_distance(self):
        return self.distance
    def get_has_index(self):
        return self.has_index
    def set_distance(self, new_distance):
        
        self.distance = new_distance
        
        if new_distance <= Point.obstacle_threshold:
            self.obstacle = True
        else:
            self.obstacle = False
            self.wall = True
        
    def set_start_wall_index(self, index):
        self.has_index = True
        self.start_wall_index = index
    def set_end_wall_index(self, index):
        self.end_wall_index = index
        self.has_index = True
    
    def set_start_w_index(self, index):
        self.has_wall_index = True
        self.start_w_index = index
    def set_end_w_index(self, index):
        self.has_wall_index = True
        self.end_w_index = index
        
    def get_start_wall_index(self):
        if self.start_wall_index is None:
            return -1
        else:
            return self.start_wall_index
    def get_end_wall_index(self):
        if self.end_wall_index is None:
            return -1
        else:
            return self.end_wall_index
        
    def set_is_obstacle(self, boolean_value):
        self.obstacle = boolean_value
    def is_obstacle (self):
        return self.obstacle
    def is_wall (self):
        return self.wall
    
    def print_point(self):
        print("Angle: ", self.angle)
        print("Distance: ", self.distance)
        print("Obstacle?: ", self.obstacle)
        print("Pos laser point: ", self.x, ", ", self.y)
    def print_obstacle_range(self):
        print("Start Obstacle Index: ", self.start_wall_index)
        print("End Obstacle Index: ", self.end_wall_index)
        print("X Coordinate: ", self.x)
        print("Y Coordinate: ", self.y)