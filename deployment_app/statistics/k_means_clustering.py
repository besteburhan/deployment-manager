import random
import numpy as np
import math
import sys
# for 2d int feature comparison


def randomly_chosen_means(k, datalist):
    min_first_feature = min(np.array(datalist)[:, 0])
    min_second_feature = min(np.array(datalist)[:, 1])
    max_first_feature = max(np.array(datalist)[:, 0])
    max_second_feature = max(np.array(datalist)[:, 1])
    cluster_centers = []
    for i in range(k):
        cluster_centers.append([random.uniform(min_first_feature + 1, max_first_feature - 1),
                                random.uniform(min_second_feature + 1, max_second_feature - 1)])
    return cluster_centers


# updating center wrt new point and old mean : (old_mean*(number_of_points-1)+new_point)/ (number_of_points)
def update_cluster_center(sz, center, data):
    center[0] = round(((center[0] * (sz - 1) + data[0]) / float(sz)), 3)
    center[1] = round(((center[1] * (sz - 1) + data[1]) / float(sz)), 3)
    return center


# the closest cluster center index to the point returns
def euclidean_distance(k, means, data):
    dist = sys.maxsize
    index = -1
    for i in range(k):
        d = (means[i][0] - data[0])**2 + (means[i][1] - data[1])**2
        d = math.sqrt(d)
        if d < dist:
            dist = d
            index = i
    return index


# with given data_dict or csv file it returns :cluster centers, data_groups(belongs to), and base data dictionary
def find_clusters(k, data_dict):
    cluster_centers = randomly_chosen_means(k, list(data_dict.values()))
    cluster_centers_sizes = [0]*k
    groups = [[] for i in range(k)]
    for t in range(100000):
        for key, data in data_dict.items():
            index = euclidean_distance(k, cluster_centers, data)
            if key in groups[index]:
                pass
            else:
                groups[index].append(key)
                cluster_centers_sizes[index] += 1
                cluster_centers[index] = update_cluster_center(cluster_centers_sizes[index],
                                                               cluster_centers[index], data)

    return cluster_centers, groups


