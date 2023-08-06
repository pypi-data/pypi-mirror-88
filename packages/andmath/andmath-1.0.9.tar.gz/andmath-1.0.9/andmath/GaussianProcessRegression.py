from .general_functions import kernel_matrix, rbf_kernel
import numpy as np
from scipy.stats import norm

class GaussianProcessRegression():
    def __init__(self, x_observed, y_observed, x_prediction=None, prediction_interval=None, N=100, sigma=1, kernel=rbf_kernel, tuner=1):
        if len(x_observed.shape)==1:
            x_observed = np.array([x_observed])
        if len(y_observed.shape)==1:
            y_observed = np.array([y_observed])

        self.x_observed = x_observed
        self.y_observed = y_observed

        if x_prediction is None:
            if prediction_interval is None:
                min = np.min(x_observed, axis=1)
                max = np.max(x_observed, axis=1)
            else:
                min = prediction_interval[0]
                max = prediction_interval[1]
            self.x_prediction = np.linspace(min, max, num=N)
        else:
            if len(x_prediction.shape)==1:
                x_prediction = np.array([x_prediction])
            if x_prediction.shape[0] == self.x_observed.shape[0]:
                self.x_prediction = x_prediction
            else:
                raise Exception('x_prediction dimension does not match x_observed.')

        self.K_observed_observed = kernel_matrix(self.x_observed, self.x_observed, kernel=kernel, tuner=tuner)
        self.K_predictive_observed = kernel_matrix(self.x_prediction, self.x_observed, kernel=kernel, tuner=tuner)
        self.K_observed_predictive = self.K_predictive_observed.T
        self.K_predictive_predictive = kernel_matrix(self.x_prediction, self.x_prediction, kernel=kernel, tuner=tuner)


        self.mean_f_star = np.dot(np.dot(self.K_predictive_observed, np.linalg.inv(self.K_observed_observed + (sigma ** 2) * np.identity(self.K_observed_observed.shape[0]))), self.y_observed.T)
        self.covariance_f_star = self.K_predictive_predictive - np.dot(np.dot(self.K_predictive_observed, np.linalg.inv(self.K_observed_observed + (sigma ** 2) * np.identity(self.K_observed_observed.shape[0]))), self.K_observed_predictive)
        self.covariance_y_star = self.covariance_f_star + (sigma ** 2) * np.identity(self.K_predictive_predictive.shape[0])

    def get_regression(self):
        return self.mean_f_star

    def get_upper_ci(self, a=0.95):
        return (self.mean_f_star.T + norm.ppf(1 - ((1 - a) / 2)) * np.sqrt(self.covariance_y_star.diagonal())).T

    def get_lower_ci(self, a=0.95):
        return (self.mean_f_star.T - norm.ppf(1 - ((1 - a) / 2)) * np.sqrt(self.covariance_y_star.diagonal())).T
