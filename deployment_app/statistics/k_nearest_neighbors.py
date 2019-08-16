import math
from .k_means_clustering import find_clusters
import matplotlib.pyplot as plt


def plotting(groups, data_dict, point, index):
    colors = ['g', 'y', 'b', 'r']
    for t in range(len(groups)):
        grouplist = groups[t]
        for i in range(len(grouplist)):
            dict_ind = grouplist[i]
            plt.scatter(data_dict[dict_ind][0],data_dict[dict_ind][1], c=colors[t])
    plt.scatter(point[0], point[1], marker='+', c=colors[index])
    plt.savefig('abc.jpeg')
    plt.close()


def knn(k, point, data_dict, groups):
    distances = []
    for cluster_index in range(len(groups)):
        for i in groups[cluster_index]:
            p = data_dict[i]
            dist = math.sqrt((point[0] - p[0])**2 + (point[1] - p[1])**2)
            distances.append([cluster_index, dist])

    distances.sort(key=lambda x: x[1])
    fist_k_dist = distances[:k]
    neighbor_counts = [0 for i in range(len(groups))]
    for dist_pair in fist_k_dist:
        neighbor_counts[dist_pair[0]] += 1
    return neighbor_counts.index(max(neighbor_counts))
