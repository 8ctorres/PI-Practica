from django.http.request import QueryDict
from django.shortcuts import render
from django.http import HttpResponse

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
        pais = request.GET['pais']
        return render(request, 'search_countries/search.html',{'pais':pais})
    else:
        return render(request, 'search_countries/search.html',{})