#import andmath as am
from andmath.GaussianProcessRegression import *
import numpy as np
import matplotlib.pyplot as plt
import time

n = 100
m = 10
mu = 0
sigma = np.sqrt(.1)

interval_observed = (0, 1)
interval_prediction = ((0, 0), (1, 1))

x_observed = np.random.uniform(interval_observed[0], interval_observed[1], (2, n))
#x_observed = np.linspace(interval_observed[0], interval_observed[1], n)
f = np.sin(x_observed[0, :] + x_observed[1, :])
y_observed = f + np.random.normal(mu, sigma, (n, 1)).T

dx1 = (interval_prediction[1][0] - interval_prediction[0][0]) / (m - 1)
dx2 = (interval_prediction[1][1] - interval_prediction[0][1]) / (m - 1)
x_prediction = np.mgrid[interval_prediction[0][0]:(interval_prediction[1][0]+dx1):dx1, interval_prediction[0][1]:(interval_prediction[1][1]+dx2):dx2].reshape((2, (m+1)*(m+1)))


i = 2
t = 10 ** (i-2)
gpr = GaussianProcessRegression(x_observed , y_observed, x_prediction, tuner=t, sigma=np.sqrt(0.1))

y_prediction = gpr.get_regression()
ci_upper = gpr.get_upper_ci()
ci_lower = gpr.get_lower_ci()

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_trisurf(x_observed[0, :], x_observed[1, :], f, label='Actual')
ax.scatter(x_observed[0, :], x_observed[1, :], y_observed[0, :], label='Observed')
ax.plot_trisurf(x_prediction[0, :], x_prediction[1, :], y_prediction[:, 0], label='Predicted')
#ax.fill_between(x_prediction[0, :].flatten(), x_prediction[1, :].flatten(), ci_upper.flatten(), ci_lower.flatten(), facecolor='orange', color='blue', alpha=0.2, label='Confidence interval')
# ax.legend(loc='upper right')
# ax.title('Tuning parameter ' + str(round(t, 4)))
#ax.xlim(np.min((interval_observed[0], interval_prediction[0])), np.max((interval_observed[1], interval_prediction[1])))
#ax.ylim(-2, 2)
#ax.axis((np.min(interval_observed[0], interval_prediction[0]), np.max(interval_observed[1], interval_prediction[1]), -2, 2))
plt.show()
