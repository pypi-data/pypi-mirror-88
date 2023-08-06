import numpy as np
import matplotlib.pyplot as plt
from .. import KMeansClustering
import time

mu_1 = .2
sigma_1 = .01

mu_2 = .6
sigma_2 = .01

mu_3 = .8
sigma_3 = .01

n = 100
d_1 = np.random.normal(mu_1, sigma_1, n)
d_2 = np.random.normal(mu_2, sigma_2, n)
d_3 = np.random.normal(mu_3, sigma_3, n)

data = np.concatenate((d_1, d_2, d_3), axis=0)
np.random.shuffle(data)

t0 = time.time()
clustering = KMeansClustering(data)
t1 = time.time()

print('Time to find clusters: ', round(1000*(t1-t0)), 'ms', sep='')

clusters = clustering.get_clusters()

n_bins=25
bins = [x/n_bins for x in range(n_bins+1)]
print(bins)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Clustering test')
ax1.hist([d_1, d_2, d_3], bins=bins, label=['Cluster 1', 'Cluster 2', 'Cluster 3'], density=True, histtype='bar', stacked=True)
ax1.legend(loc='upper left')
ax1.set_title('Actual clusters')

ax2.hist([data[clusters==0], data[clusters==1], data[clusters==2]], bins=bins, label=['Cluster 1', 'Cluster 2', 'Cluster 3'], density=True, histtype='bar', stacked=True)
ax2.legend(loc='upper left')
ax2.set_title('K-Means clusters')

plt.show()
