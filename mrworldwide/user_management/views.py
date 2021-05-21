from curses import A_ALTCHARSET
from django.shortcuts import render,redirect
from flask import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from websockets import auth
from .schemas import login_schema, signup_schema

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
	logout(request)
	return redirect(request.GET['next'])

def signup_view(request):
	if request.method == 'GET':
		return render(request,'signup.html')
	if request.method == 'POST':
		try:
			validate(instance=request.POST, schema=signup_schema)
			username,email,password = request.POST
			new_user = User.objects.create_user(username, email,password)
			new_user.save()
			user = authenticate(username=request.POST.username, password=request.POST.password)
			login(request,user)
			return redirect('profile_view')
		except ValidationError:
			return render(request,'login.html', {'error': 'Invalid parameters'})
		except:
			return render(request,'login.html', {'error': 'Unexpected error'})


def profile_view(request):
	return render(request,'profile.html')