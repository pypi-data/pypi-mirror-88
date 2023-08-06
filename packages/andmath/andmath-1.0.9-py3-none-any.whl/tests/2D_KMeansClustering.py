import numpy as np
import matplotlib.pyplot as plt
from .. import KMeansClustering
import time

mu_1 = [1, .5]
Sigma_1 = np.array([[1, 0], [0, 1]])

mu_2 = [4, 2.5]
Sigma_2 = np.array([[1, .2], [.2, 1]])

mu_3 = [3, .5]
Sigma_3 = np.array([[1, -.5], [-.5, 1]])

n = 100
d_1 = np.random.multivariate_normal(mu_1, Sigma_1, n)
d_2 = np.random.multivariate_normal(mu_2, Sigma_2, n)
d_3 = np.random.multivariate_normal(mu_3, Sigma_3, n)

data = np.concatenate((d_1, d_2, d_3), axis=0)
np.random.shuffle(data)

K=3
t0 = time.time()
clustering = KMeansClustering(data, K=K)
t1 = time.time()

print('Time to find clusters: ', round(1000*(t1-t0)), 'ms', sep='')

clusters = clustering.get_clusters()

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Clustering test')
plot_1_1, = ax1.plot(d_1[:,0], d_1[:,1], 'o', label='Cluster 1')
plot_1_2, = ax1.plot(d_2[:,0], d_2[:,1], 'o', label='Cluster 2')
plot_1_3, = ax1.plot(d_3[:,0], d_3[:,1], 'o', label='Cluster 3')
ax1.legend(handles=[plot_1_1, plot_1_2, plot_1_3,], loc='upper left')
ax1.set_title('Actual clusters')

plots = []
for k in range(K):
    plot, = ax2.plot(data[(clusters==k), 0], data[(clusters==k), 1], 'o', label='Cluster '+str(k+1))
    plots.append(plot)
ax2.legend(handles=plots, loc='upper left')
ax2.set_title('K-Means clusters')

plt.show()
