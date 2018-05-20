from .user_information import UserInformation
from .dataset_manipulation import DatasetManipulation
from .problem_information import ProblemInformation
from scipy import spatial

class Recommendation():
    @staticmethod
    def find_closest_problem(theta_user, theta_problems, aggressivity_radius):
        problems = [problem for problem in theta_problems if (
            theta_problems[problem] > theta_user).any()]
        points = [theta_problems[problem] for problem in problems]
        nr_points = len(points)

        if not points:
            return None

        tree = spatial.KDTree(points)
        distances, indexes = tree.query(theta_user, k=nr_points)

        if nr_points == 1:
            distances = [distances]
            indexes = [indexes]

        for distance, index in zip(distances, indexes):
            if distance > aggressivity_radius:
                return problems[index]

        return None

    @staticmethod
    def get_next_problem(
            problems_solved,
            thetas,
            nr_features,
            aggressivity_radius
        ):
        thetas_solved = {}
        thetas_not_solved = {}

        for theta in thetas:
            if theta in problems_solved:
                thetas_solved[theta] = thetas[theta]
            else:
                thetas_not_solved[theta] = thetas[theta]

        if not thetas_not_solved:
            return None

        theta_user = UserInformation.get_theta_of_user(problems_solved, thetas_solved, nr_features)
        problem = Recommendation.find_closest_problem(
            theta_user, thetas_not_solved, aggressivity_radius)

        return problem
    
    @staticmethod
    def get_thetas(solutions_df, nr_features, nr_epochs, nr_iterations):
        thetas = {}

        i = 0
        i_max = len(
            DatasetManipulation.get_problems_from_solutions(solutions_df)
        )
        
        for problem in DatasetManipulation.get_problems_from_solutions(solutions_df):
            matrix = DatasetManipulation.get_solution_matrix(
                solutions_df, problem)
            theta = ProblemInformation.get_theta_of_problem(
                matrix,
                nr_features,
                nr_epochs,
                nr_iterations
            )
            thetas[problem] = theta

            print('Progress: {}%'.format(100 * i / i_max))
            i += 1
        import pdb; pdb.set_trace()
        return thetas
