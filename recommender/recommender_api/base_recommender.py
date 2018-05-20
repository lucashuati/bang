import numpy as np

class BaseRecommender():
    
    @staticmethod
    def gradient_descent(x, y, nr_iterations, alpha=0.01):
        # m - number of samples
        # n - number features
        m, n = x.shape

        # insert column theta_zero = 1
        x = np.c_[np.ones(m), x]

        theta = np.ones(n + 1)
        x_transpose = x.transpose()

        for _ in range(0, nr_iterations):
            hypothesis = np.dot(x, theta)
            loss = hypothesis - y
            gradient = np.dot(x_transpose, loss) / m
            theta = theta - alpha * gradient

        return theta
