import numpy as np
from .base_recommender import BaseRecommender

class ProblemInformation():   
    @staticmethod
    def get_theta_of_problem(matrix, nr_features, nr_epochs, nr_iterations):
        nr_problems, nr_users = matrix.shape

        theta_users = np.random.rand(nr_users, nr_features)
        theta_problems = np.zeros((nr_problems, nr_features))

        matrix_t = np.transpose(matrix)

        i = 0
        while i <= nr_epochs:
            print('Progress: {}%'.format(100 * i/nr_epochs))
            i += 1

            for problem in range(nr_problems):
                x = np.array(
                    theta_users
                )

                y = np.array(
                    matrix[problem]
                )

                theta_problems[problem] = BaseRecommender.gradient_descent(x, y, nr_iterations)[
                    1:]

            for user in range(nr_users):
                x = np.array(
                    theta_problems
                )

                y = np.array(
                    matrix_t[user]
                )

                theta_users[user] = BaseRecommender.gradient_descent(x, y, nr_iterations)[1:]

        return theta_problems.mean(axis=0)
