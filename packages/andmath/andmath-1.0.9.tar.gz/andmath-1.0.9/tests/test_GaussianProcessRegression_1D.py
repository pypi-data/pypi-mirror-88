#import andmath as am
from andmath.GaussianProcessRegression import *
import numpy as np
import matplotlib.pyplot as plt
import time

n = 9*12+1
m = 12*12+1
mu = 0
sigma = np.sqrt(.1)

interval_observed = (0, 9)
interval_prediction = (0, 12)

#x_observed = np.random.uniform(interval_observed[0], interval_observed[1], n)
x_observed = np.linspace(interval_observed[0], interval_observed[1], n)
f = np.tanh(2 * np.pi * x_observed / 12) - 0.1 * (x_observed- (interval_observed[1] - interval_observed[0]) / 2)
y_observed = f + np.random.normal(mu, sigma, n)

x_prediction = np.linspace(interval_prediction[0], interval_prediction[1], m)

fig = plt.figure()
for i in range(4):
    t = 10 ** (i-2)
    gpr = GaussianProcessRegression(x_observed , y_observed, x_prediction, tuner=t, sigma=np.sqrt(0.1))

    y_prediction = gpr.get_regression()
    ci_upper = gpr.get_upper_ci()
    ci_lower = gpr.get_lower_ci()

    ind = np.argsort(x_prediction)
    x_prediction = x_prediction[ind]
    y_prediction = y_prediction[ind]
    ci_upper = ci_upper[ind]
    ci_lower = ci_lower[ind]

    plt.subplot(2, 2, i+1)
    plt.tight_layout()
    plt.plot(x_observed, f, 'b-', label='Actual')
    plt.plot(x_observed, y_observed, 'go', label='Observed')
    plt.plot(x_prediction, y_prediction, 'r-', label='Predicted')
    plt.fill_between(x_prediction.flatten(), ci_upper.flatten(), ci_lower.flatten(), facecolor='orange', color='blue', alpha=0.2, label='Confidence interval')
    plt.legend(loc='upper right')
    plt.title('Tuning parameter ' + str(round(t, 4)))
    plt.xlim(np.min((interval_observed[0], interval_prediction[0])), np.max((interval_observed[1], interval_prediction[1])))
    #plt.ylim(-2, 2)
    #plt.axis((np.min(interval_observed[0], interval_prediction[0]), np.max(interval_observed[1], interval_prediction[1]), -2, 2))
plt.show()
