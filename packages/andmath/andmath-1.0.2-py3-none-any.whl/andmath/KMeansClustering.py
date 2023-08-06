import numpy as np
from .general_functions import get_centroid, get_distance

class KMeansClustering():
    def __init__(self, data, K=3, max_iterations=1000):
        if len(data.shape)==1:
            data = np.array([data]).T
        self.data = data
        self.K = K
        self.D = self.data.shape[1]
        self.N = self.data.shape[0]
        self.clusters =  np.random.randint(K, size=self.N)
        self.centroids = self.__get_centroids__()
        self.max_iterations = max_iterations
        self.max_number_of_tries = 950
        self.iterate()

    def get_clusters(self):
        return self.clusters

    def iteration(self):
        centroids = self.__get_centroids__()
        clusters = np.zeros(self.N)
        for n in range(self.N):
            distances = np.zeros((self.K))
            for k in range(self.K):
                distances[k] = get_distance(self.data[n, :], centroids[k, :])
            clusters[n] = np.argmin(distances)
        return clusters, centroids

    def iterate(self, try_number=0, max_iterations=None):
        if max_iterations is None:
            max_iterations = self.max_iterations
        i = 0
        while i < max_iterations:
            clusters, centroids = self.iteration()
            if np.unique(clusters).shape[0] < self.K:
                if try_number < self.max_number_of_tries:
                    self.clusters =  np.random.randint(self.K, size=self.N)
                    self.centroids = self.__get_centroids__()
                    return self.iterate(try_number=try_number+1)
                print('No solution could be found.')
                return self.clusters, self.centroids
            if (clusters==self.clusters).all():
                print('Solution found after ' + str(i) + ' iterations.')
                return clusters, centroids
            self.clusters, self.centroids = clusters, centroids
            i += 1
        if i==max_iterations:
            print('Maximum iteration reached. Will return the last cluster.')
            return clusters, centroids

    def __get_centroids__(self):
        centroids = np.zeros((self.K, self.D))
        for k in range(self.K):
            centroids[k, :] = get_centroid(self.data[self.clusters==k, :])
        return centroids
