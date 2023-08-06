import numpy as np

def l2_norm(x, y):
    return np.linalg.norm(x - y)

def mean(matrix):
    return np.average(matrix, axis=0)

def get_centroid(matrix, centroid_method=mean):
    return centroid_method(matrix)

def get_distance(x, y, distance_metric=l2_norm):
    return distance_metric(x, y)
