from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    context = {'search_country' : 'Spain'}
    return redirect("search") #TODO pasar el parámetro
