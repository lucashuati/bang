from .recommendation import Recommendation
from .recommender import Recommender
import pandas as pd
import os

class UriRecommender(Recommender):
    def __init__(self):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(
            file_path, 'data_files/solutions_uri.csv'
        )
    
    def load_solutions(self, category=None):
        solutions_df = pd.read_csv(self.data_file)
        if category:
            solutions_df = solutions_df.loc[solutions_df['category_id'] == category]
            solutions_df = solutions_df.loc[solutions_df['solved'] > 100]
        return solutions_df
    
    def generate_thetas(self, category=None):
        solutions_df = self.load_solutions(category)
        thetas = Recommendation.get_thetas(
            solutions_df,
            nr_features=self.NR_FEATURES,
            nr_epochs=self.NR_EPOCHS,
            nr_iterations=self.NR_ITERATIONS
        )
        return thetas

    def next_problem(self, thetas, problems_solved=[]):
        return Recommendation.get_next_problem(
            problems_solved,
            thetas,
            nr_features=self.NR_FEATURES,
            aggressivity_radius=self.AGGRESSIVITY_RADIUS
        )

    def run(self, category=None, problems_solved=[]):
        thetas = self.generate_thetas(category)
        # Thetas already calculated for math category(5)
        # thetas = pd.read_csv('data_files/thetas.csv')
        # thetas = thetas.to_dict('list')
        return self.next_problem(thetas, problems_solved)
