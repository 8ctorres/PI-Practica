from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from django.db.utils import IntegrityError
from .schemas import login_schema, signup_schema
from django.utils.datastructures import MultiValueDictKeyError
from .models import Profile,MultipleIndicatorChart,SingleIndicatorChart
import traceback

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
	if request.method == 'GET' and request.user.is_authenticated:
		user = User.objects.get(username=request.user)
		profile = Profile.objects.get(user=user)
		print(user)
		context = {'single_indicator': profile.single_indicator.all(), 'multiple_indicators': profile.multiple_indicators.all()}
		return render(request,'profile.html',context)
	if request.method == 'GET':
		return redirect('login')
	if request.method == 'POST' and request.user.is_authenticated:
		try:
			user = User.objects.get(username=request.user)
			profile = Profile.objects.get(user=user)
			chart_type = request.POST['chart-type']
			image = request.POST['image']
			if chart_type == "SingleIndicatorChart":
				indicator = request.POST['indicator']
				chart = SingleIndicatorChart(indicator=indicator, image=image)
				chart.save()
				profile.single_indicator.add(chart)
			elif chart_type == "MultipleIndicatorChart":
				country = request.POST['country']
				chart = MultipleIndicatorChart(country=country, image=image)
				chart.save()
				profile.multiple_indicators.add(chart)
			else:
				context = {'error': 'Invalid chart type'}
			context = {'single_indicator': profile.single_indicator.all(), 'multiple_indicators': profile.multiple_indicators.all()}
		except MultiValueDictKeyError:
			context = {'error': 'Invalid data'}
		except Exception:
			traceback.print_exc()
			context = {'error': 'Unexpected error'}
		return render(request,'profile.html',context)

def delete_chart(request):
	if request.method == 'POST' and request.user.is_authenticated:
		try:
			graph_id = request.POST['chart-id']
			graph_type = request.POST['chart-type']
			user = User.objects.get(username=request.user)
			profile = Profile.objects.get(user=user)
			if graph_type == "SingleIndicatorChart":
				graph = profile.single_indicator.get(pk=graph_id)
				profile.single_indicator.remove(graph)
				SingleIndicatorChart.objects.filter(id=graph_id).delete()
			elif graph_type == "MultipleIndicatorChart":
				graph = profile.multiple_indicators.get(pk=graph_id)
				profile.multiple_indicators.remove(graph)
				MultipleIndicatorChart.objects.filter(id=graph_id).delete()
		except MultiValueDictKeyError:
			return HttpResponse('400 Bad Request', status=400)
		except Exception:
			return HttpResponse('500 Server Error', status=500)
		return redirect('login',)

