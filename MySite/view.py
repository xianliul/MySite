# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
 
def home(request):
    context          = {}
    return render(request, 'home.html', context)
def register(request):
    context          = {}
    return render(request, 'register.html', context)
def login(request):
    context          = {}
    return render(request, 'login.html', context)