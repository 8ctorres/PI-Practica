from django.shortcuts import render,redirect

# Create your views here.
def login_view(request):
	return render(request,'login.html')

def logout_view(request):
	return redirect(request.GET['next'])

def signup_view(request):
	return render(request,'signup.html')