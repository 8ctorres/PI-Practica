from django.shortcuts import render
from django.http import HttpResponse
from mrworldwide.models import Pais

# Create your views here.
def homepage(request):
    return render(request, 'homepage/home.html')