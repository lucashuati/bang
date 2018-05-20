import numpy as np
from .base_recommender import BaseRecommender

class DatasetManipulation():
    @staticmethod
    def get_problems_from_solutions(solutions_df):
        problems = set(solutions_df['problem_id'])

        return list(problems)

    @staticmethod
    def get_users_that_solved_the_problem(solutions_df, problem_id):
        solutions_of_the_problem_df = solutions_df[solutions_df['problem_id'] == problem_id]
        users = solutions_of_the_problem_df['user_id']

        return list(users)

    @staticmethod
    def get_date_when_user_solved_the_problem(solutions_df, user_id, problem_id):
        solution = solutions_df[(solutions_df['problem_id'] == problem_id) & (
            solutions_df['user_id'] == user_id)]
        solution_date = solution['date'].values[0]

        return solution_date

    @staticmethod
    def get_past_problems(solutions_df, user_id, problem_id):
        solution_date = DatasetManipulation.get_date_when_user_solved_the_problem(
            solutions_df, user_id, problem_id)
        past_solutions = solutions_df[(solutions_df['date'] < solution_date) & (
            solutions_df['user_id'] == user_id)]
        problems = past_solutions['problem_id']

        return list(problems)

    @staticmethod
    def optimize_matrix(matrix):
        matrix = matrix[~np.all(matrix == 0., axis=1)]
        return matrix

    @staticmethod
    def get_solution_matrix(solutions_df, problem):
        users = DatasetManipulation.get_users_that_solved_the_problem(
            solutions_df, problem)

        solutions = []
        min_problem = float('inf')
        max_problem = float('-inf')

        for user in users:
            past_problems = DatasetManipulation.get_past_problems(
                solutions_df, user, problem)

            solutions.append(past_problems)

            min_problem = min([min_problem] + past_problems)
            max_problem = max([max_problem] + past_problems)

        nr_problems = max_problem - min_problem + 1
        nr_users = len(users)
        matrix = np.zeros((nr_problems, nr_users))

        for user in range(nr_users):
            for problem in solutions[user]:
                problem_index = problem - min_problem
                matrix[problem_index][user] = 1

        return DatasetManipulation.optimize_matrix(matrix)
