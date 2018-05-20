import json
import errno
import os
from recommender.recommender_api.uri_recommender import UriRecommender
from bang.settings import BASE_DIR
from recommender.models import Recommender, RecommenderCategory, RecommenderThetas
from home.models import Problem
AVAILABLE_JUDGES = ['uri']


def get_recommender(judge):
    recommender = Recommender.objects.filter(judge=judge).first()
    return recommender

def has_category(recommender, category_id):
    category = RecommenderCategory.objects.filter(
        recommender=recommender,
        category_id_judge=category_id
    )
    return category.count() != 0

def validate_data(data):
    judge = data.get('judge')
    category = data.get('category')
    if judge:
        if judge.lower() not in AVAILABLE_JUDGES:
            return False, '{} is not avaiable.'.format(judge)
    else:
        return False, 'Judge not found.'

    if category:
        name = category.get('name')
        category_id = category.get('categoryIdJudge')
        if not name:
            return False, 'Category name not found.'
        if category_id:
            recommender = get_recommender(judge.lower())
            if has_category(recommender, category_id):
                 return False, 'Category has calculated.'
        else:
            return False, 'Category name not found.'
    else:
       return False, 'Category not found.'
    return True, 'Data is available'

def get_problem(code, judge):
    return Problem.objects.get(code=code, judge=judge)

def crate_category(judge, category_name, category_id):
    recommender = get_recommender(judge)
    return RecommenderCategory.objects.create(
        recommender=recommender,
        name=category_name,
        category_id_judge=category_id
    )
    
def run(*args):
    """
        RUN: python manage.py runscript generate_thetas --script-args 
            <config_path>
    """
    if args:
        data = None
        try:
            file_path = os.path.join(BASE_DIR, args[0])
            with open(file_path) as f:
                data = json.load(f)
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('Config file not found')
        except json.decoder.JSONDecodeError:
            print('JSON invalid')
        
        if data:
            for judge_category in data:
                valid, mensage = validate_data(judge_category)
                if valid:
                    recommender_category = crate_category(
                        judge_category['judge'],
                        judge_category['category']['name'],
                        judge_category['category']['categoryIdJudge']
                    )
                    uri_recommender = UriRecommender()
                    thetas = uri_recommender.generate_thetas(
                        category=judge_category["category"]["categoryIdJudge"]
                    )
                    for problem_theta in thetas:
                        RecommenderThetas.objects.create(
                            values=thetas[problem_theta].tolist(),
                            recommeder_category=recommender_category,
                            problem=get_problem(
                                problem_theta,
                                judge_category['judge'].lower()
                            )
                        )
                    print(
                        'Thetas for [{}]{} has been calculated'.format(
                            judge_category['judge'],
                            judge_category['category']['name']
                        )
                    )
                else:
                    print(mensage)        


