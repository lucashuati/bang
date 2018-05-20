from django.db import models
from django.contrib.postgres.fields import ArrayField
from home.models import Problem

class Recommender(models.Model):
    judge = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Recommender'
        verbose_name_plural = 'Recommenders'

    def __str__(self):
        return '{} Recommender'.format(self.judge)


class RecommenderCategory(models.Model):
    name = models.CharField(max_length=100)
    recommender = models.ForeignKey(Recommender, on_delete=models.CASCADE)
    category_id_judge = models.IntegerField()

    class Meta:
        verbose_name = 'Recommender Category'
        verbose_name_plural = 'Recommender Categories'

    def __str__(self):
        return '[{}]: {}'.format(self.recommender, self.name)

class RecommenderThetas(models.Model):
    values = ArrayField(
        models.FloatField()
    )
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    recommeder_category = models.ForeignKey(RecommenderCategory, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Recommender Thetas'
        verbose_name_plural = 'Recommenders Thetas'
    
    def __str__(self):
        return self.problem.__str__()
