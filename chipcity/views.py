from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json
from chipcity.models import Game, Player, StuffCard


def onLoad(request):
        # return render(request, 'socialnetwork/login.html')
        # Display splash art page intsead of redirecting
        return redirect(reverse('join_action'))
    

# Create your views here.
def splash_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'splash.html', context)
    return render(request, 'splash.html', context)

@login_required
def join_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'join.html', context)
    return render(request, 'join.html', context)

@login_required
def table_action(request):
    context = {}
    # if request.method == 'GET':
    #     return render(request, 'table.html', context)
    
    # we want to create a game instance 
    new_game = Game()
    new_game.create_game(game_num=1, num_players=0, init_pot=0,curr_round=0)
    new_game.save()
    
    return render(request, 'table.html', context)

