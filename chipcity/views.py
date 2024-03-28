from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json
from.models import*


def onLoad(request):
        # return render(request, 'socialnetwork/login.html')
        return redirect(reverse('join_action'))
    

# Create your views here.
# @login_required
def join_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'join.html', context)
    return render(request, 'join.html', context)
    
def table_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'table.html', context)
    if request.method == 'POST':
        new_game=Game(dealer=request.player, num_of_players=1, user=request.player, creation_time=timezone.now())
        new_game.save()
        context['game'] = new_game 
    return render(request, 'table.html', context)

@login_required
def login_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'login.html', context)
    return render(request, 'login.html', context)
     
