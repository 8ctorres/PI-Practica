from django.http.request import QueryDict
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pais

# Create your views here.
""" def search_countries(request):
    if request.method == 'GET':
        queryDict = request.GET.dict()
        if 'pais' in queryDict:
            context = {'pais':1}
        else:
            context = dict()
        return render(request, 'search_countries/search.html', context) """
        
def search_countries(request):
    if request.method == 'GET':
        busqueda = request.GET['busqueda']
        pais = Pais.objects.filter(name__contains=busqueda)
        return render(request, 'search_countries/search.html',{'busqueda':busqueda, 'pais':pais})
    else:
        return render(request, 'search_countries/search.html',{})