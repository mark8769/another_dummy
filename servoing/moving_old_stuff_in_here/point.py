class Point():
    
    def __init__(self, x, y, distance, angle):
      
      self.x = x
      self.y = y
      self.distance = distance
      self.angle = angle
      # TODO: Get rid of this instance variable?
      self.start_wall_index = None
      self.end_wall_index = None
      self.has_index = False
      # for preprocessing of laser point cloud data
      # part B in paper
      if distance <= 80:
          self.obstacle = True
      else:
          self.obstacle = False
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_angle(self):
        return self.angle
    def get_distance(self):
        return self.distance
    def set_distance(self, new_distance):
        
        self.distance = new_distance
        
        if new_distance <= 80:
            self.obstacle = True
        else:
            self.obstacle = False
            
    def set_start_wall_index(self, index):
        self.has_index = True
        self.start_wall_index = index
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
        
    def get_has_index(self):
        return self.has_index
    def set_end_wall_index(self, index):
        self.end_wall_index = index
        self.has_index = True
    def is_obstacle (self):
        return self.obstacle
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