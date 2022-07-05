import simulated_environment as se
import numpy
from obstacle_detection_helper import visualize_points
from obstacle_detection import(
    median_filtering_two_pass,
    preprocessing_laser_point,
    add_clusters
)

def get_dummy_data():

    visualize_points(se.lidar_points)
    filtered_points = numpy.empty([1, len(se.lidar_points[0])], dtype=object)
    filtered_points, _ = median_filtering_two_pass(se.lidar_points)
    
    filtered_points = preprocessing_laser_point(filtered_points)
    cluster_list = add_clusters(filtered_points)
    print()
    print("-------------------------------------FILTERED POINTS------------------------------------------------")
    visualize_points(filtered_points)

    temp_max = 0
    temp_cluster = None
    for cluster in cluster_list:

        temp_range = cluster.get_end_index() - cluster.get_start_index()
        if temp_range >= temp_max:
            temp_max = temp_range
            temp_cluster = cluster

    if temp_cluster is None:
        return None, None
    else:
        print("Acquired object")
        
    distance = temp_cluster.get_center_distance()
    angle = temp_cluster.get_center_angle()

    if angle <= 0:
        angle = abs(angle) + 90
    else:
        angle = abs(angle - 90)

    return distance, angle


def main():

    distance, angle = get_dummy_data()
    print("Distance Acquired: ", distance)
    print("Angle Acquired: ", angle)
    distance, angle = get_dummy_data()
    print("Distance Acquired: ", distance)
    print("Angle Acquired: ", angle)
    
if __name__ == '__main__':
    main()