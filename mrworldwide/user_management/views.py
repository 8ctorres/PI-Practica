from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from flask import request

# Create your views here.
def login_view(request):
	if request.method == 'GET':
		return render(request,'login.html')
	elif request.method == 'POST':
		return render(request,'login.html')

def logout_view(request):
	return redirect(request.GET['next'])

def signup_view(request):
	if request.method == 'GET':
		return render(request,'signup.html')
	if request.method == 'POST':
		return redirect('index')

def profile_view(request):
	return render(request,'profile.html')