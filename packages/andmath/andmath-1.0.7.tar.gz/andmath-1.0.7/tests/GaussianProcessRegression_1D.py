import andmath as am
import numpy as np
import matplotlib.pyplot as plt
import time

n = 100
mu = 0
sigma = .1

interval_observed = (0, 1)
interval_prediction = (0, 1)

x_observed = np.random.uniform(interval_observed[0], interval_observed[1], n)
y_observed = np.sin(2 * np.pi * x_observed) + np.random.normal(mu, sigma, n)

x_prediction = np.linspace(interval_prediction[0], interval_prediction[1], n)

gpr = GaussianProcessRegresssion(x_observed , y_observed, x_prediction)

y_prediction = gpr.get_regression()

ind = np.argsort(x_prediction)
x_prediction = x_prediction[ind]
y_prediction = y_prediction[ind]

fig = plt.figure()
plots = []
plot = plt.plot(x_observed, y_observed, 'o', label='Observed')
plots.append(plot)
plot = plt.plot(x_prediction, y_prediction, '-', label='Predicted')
plots.append(plot)
plt.legend(plots)
plt.axis((np.min(interval_observed[0], interval_prediction[0]), np.max(interval_observed[1], interval_prediction[1]), -2, 2))
plt.show()
