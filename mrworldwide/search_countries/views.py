from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def search_countries(request):
    return render(request, 'search_countries/search.html')