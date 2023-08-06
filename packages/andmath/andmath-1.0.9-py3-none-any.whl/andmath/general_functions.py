import numpy as np

def l2_norm(x, y=None):
    if y is None:
        return np.linalg.norm(x)
    else:
        return np.linalg.norm(x - y)

def mean(matrix, axis=0):
    return np.average(matrix, axis=axis)

def get_centroid(matrix, centroid_method=mean):
    return centroid_method(matrix)

def get_distance(x, y, distance_metric=l2_norm):
    return distance_metric(x, y)

def rbf_kernel(x, y, sigma=1, norm=l2_norm):
    return np.exp(-(norm(x, y) ** 2) / (2 * (sigma ** 2)))

def kernel_matrix(x, y, kernel=rbf_kernel, tuner=1):
    m = x.shape[1]
    n = y.shape[1]
    mat = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            mat[i, j] = kernel(x[:, i], y[:, j], tuner)
    return mat
