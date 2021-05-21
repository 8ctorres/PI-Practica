from curses import A_ALTCHARSET
from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest
from flask import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from .schemas import login_schema

# Create your views here.
def login_view(request):
	if request.method == 'GET':
		return render(request,'login.html')
	elif request.method == 'POST':
		try:
			validate(instance=request.POST, schema=login_schema)
			user = authenticate(username=request.POST.username, password=request.POST.password)
			if user is not None:
				login(request, user)
				return redirect(request.GET['next'])
			else:
				print("error")
				return render(request,'login.html',{'error': 'Invalid credentials'})
		except ValidationError:
			return render(request,'login.html', {'error': 'Invalid parameters'})
		except:
			return render(request,'login.html', {'error': 'Unexpected error'})

def logout_view(request):
	return redirect(request.GET['next'])

def signup_view(request):
	if request.method == 'GET':
		return render(request,'signup.html')
	if request.method == 'POST':
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user.save()
		return render(request,'signup.html')

def profile_view(request):
	return render(request,'profile.html')