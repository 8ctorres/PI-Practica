import traceback
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from django.db.utils import IntegrityError
from .schemas import login_schema, signup_schema


# Create your views here.
def login_view(request):
	if request.method == 'GET' and request.user.is_authenticated:
		return redirect('profile')
	if request.method == 'GET':
		return render(request,'login.html')
	if request.method == 'POST':
		try:
			validate(instance=request.POST, schema=login_schema)
			queryDict = request.POST.dict()
			unpackedBody = [ queryDict[key] for key in ["username","password"] ]
			username,password = unpackedBody
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('profile')
			else:
				context = {'error': 'Invalid credentials'}
		except ValidationError:
			context = {'error': 'Invalid parameters'}
		except:
			context = {'error': 'Unexpected error'}
		return render(request,'login.html',context)

def logout_view(request):
	if request.method == 'GET' and request.user.is_authenticated:
		logout(request)
		return redirect('login')

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('profile')
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
			return redirect('profile')
		except ValidationError:
			context = {'error': 'Invalid parameters'}
		except IntegrityError:
			context = {'error': 'User already exists'}
		except:
			context = {'error': 'Unexpected error'}
		return render(request,'signup.html',context)


def profile_view(request):
	if request.method == 'GET' and (not request.user.is_authenticated):
		return redirect('login')
	if request.method == 'GET':
		return render(request,'profile.html')