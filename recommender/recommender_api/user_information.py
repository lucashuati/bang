import numpy as np

class UserInformation():
    @staticmethod
    def get_theta_of_user(problems_solved, thetas_solved, nr_features):
        if not problems_solved:
            return np.zeros(nr_features)

        thetas = [thetas_solved[t] for t in thetas_solved]
        theta_of_user = np.max(thetas, axis=0)

        return theta_of_user
