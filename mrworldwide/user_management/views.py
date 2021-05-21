from django.shortcuts import render,redirect
from flask import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from sqlite3 import IntegrityError
from .schemas import login_schema, signup_schema

# Create your views here.
def login_view(request):
	if request.user.is_authenticated:
		return redirect('profile_view')
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
				context = {'error': 'Invalid credentials'}
		except ValidationError:
			context = {'error': 'Invalid parameters'}
		except:
			context = {'error': 'Unexpected error'}
		return render(request,'login.html',context)

def logout_view(request):
	if request.method == 'POST' and request.user.is_authenticated:
		logout(request)
		return redirect(request.GET['next'])

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('profile_view')
	if request.method == 'GET':
		return render(request,'signup.html')
	if request.method == 'POST':
		try:
			validate(instance=request.POST, schema=signup_schema)
			queryDict = request.POST.dict()
			unpackedBody = [ queryDict[key] for key in ["username","email","password"] ]
			username,email,password = unpackedBody
			new_user = User.objects.create_user(username, email,password)
			new_user.save()
			user = authenticate(username=username, password=password)
			login(request,user)
			return redirect('profile_view')
		except ValidationError:
			context = {'error': 'Invalid parameters'}
		except IntegrityError:
			context = {'error': 'User already exists'}
		except:
			traceback.print_exc()
			context = {'error': 'Unexpected error'}
		return render(request,'signup.html',context)


def profile_view(request):
	return render(request,'profile.html')