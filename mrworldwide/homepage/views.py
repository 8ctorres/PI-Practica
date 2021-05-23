from django.shortcuts import render, redirect
from django.http import HttpResponse
from apis.restcountries import get_countries_by_name

# Create your views here.
def homepage(request):
    return redirect("search") #TODO pasar el parámetro
