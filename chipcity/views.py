from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json


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
    if request.method == 'GET':
        return render(request, 'table.html', context)
    return render(request, 'table.html', context)
