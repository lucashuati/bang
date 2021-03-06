from django.shortcuts import render
from home.models import Solution, Problem
from django.contrib.auth.decorators import login_required
# Create your views here.

def uri():
	return Solution.objects.filter(problem__judge='uri').order_by('problem__code').distinct('problem__code')

def uva():
	return Solution.objects.filter(problem__judge='uva').order_by('problem__number').distinct('problem__number')

def spoj():
	return Solution.objects.filter(problem__judge='spoj').order_by('problem__code').distinct('problem__code')

@login_required
def problems(request):
	context = {
		'uri' : uri(),
		'uva' : uva(),
		'spoj' : spoj(),
	}

	return render(request, 'problems/problems.html', context)

@login_required
def problem(request, problem_id):
	solutions = Solution.objects.filter(problem__id=problem_id)
	problem = solutions[0].problem
	context = {
		'problem' : problem,
		'solutions' : solutions,
	} 
	return render(request, 'problems/problem.html', context)