from .general_functions import get_kernel_matrix

class GaussianProcessRegresssion():
    def __init__(self, x_observed, y_observed, x_prediction=None, prediction_interval=None, N=100, sigma = 1):
        if len(x_observed.shape)==1:
            x_observed = np.array([x_observed]).T
        if len(y_observed.shape)==1:
            y_observed = np.array([y_observed]).T

        print('Gaussian Process')

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
                x_prediction = np.array([x_prediction]).T
            if x_prediction.shape[1] == self.x_observed.shape[1]:
                self.x_prediction = x_prediction
            else:
                raise Exception('x_prediction dimension does not match x_observed.')

        self.K_observed_observed = matrix_kernel(self.x_observed, self.x_observed)
        self.K_predictive_observed = matrix_kernel(self.x_prediction, self.x_observed)
        self.K_observed_predictive = self.K_predictive_observed.T
        self.K_predictive_predictive = matrix_kernel(self.x_prediction, self.x_prediction)

        self.mean_f_star = np.dot(np.dot(self.K_predictive_observed, np.linalg.inv(self.K_observed_observed + sigma * np.identity(self.K_observed_observed.shape[0]))), t(Y_observed))
        self.covariance_f_star = self.K_predictive_predictive - np.dot(np.dot(self.K_predictive_observed, np.linalg.inv(self.K_observed_observed + sigma * np.identity(self.K_observed_observed.shape[0]))), self.K_observed_predictive)
        self.covariance_y_star = self.covariance_f_star + sigma * np.identity(self.K_observed_observed.shape[0])

    def get_regression():
        return mean_f_star
