from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from home.utils import *


def login(request):
    return render(request, 'home/login.html')


@login_required
def about(request):
    return render(request, 'home/about.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required
@user_passes_test(group_check, login_url='/groups')
def home(request):
    if request.user.is_superuser:
        auth_logout(request)
        return redirect('/')

    context = {
        'group': getSolutionsAmount(),
        'events': getEvents(),
        'trends': getTrends(),
        'historic': getHistoric(),
        'recentlySolved': getLastSolutions(),
    }

    return render(request, 'home/home.html', context)
''