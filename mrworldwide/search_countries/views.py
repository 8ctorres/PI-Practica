from django.http.request import QueryDict
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pais
from apis.restcountries import get_countries_by_name
from apis.exceptions import APIRequestException

# Create your views here.        
def search_countries(request):
    if request.method == 'GET':
        search_country = request.GET['search_country']
        try:
            country_data = get_countries_by_name(search_country)
            name = country_data.iloc[0][0]
            TLD = country_data.iloc[0][1]
            ISO = country_data.iloc[0][2]
            phone_prefix = country_data.iloc[0][3]
            Capital = country_data.iloc[0][4]
            AltNames = country_data.iloc[0][5]
            Region = country_data.iloc[0][6]
            Subregion = country_data.iloc[0][7]
            Poblation = country_data.iloc[0][8]
            Coordinates = country_data.iloc[0][9]
            Gentilicio = country_data.iloc[0][10]
            Superficie = country_data.iloc[0][11]
            Gini = country_data.iloc[0][12]
            timezone = country_data.iloc[0][13]
            borderlines = country_data.iloc[0][14]
            native_language = country_data.iloc[0][15]
            codeX = country_data.iloc[0][16]
            coin = country_data.iloc[0][17]
            oficial_language = country_data.iloc[0][18]
            flag = country_data.iloc[0][19]
            asociations = country_data.iloc[0][20]
            return render(request, 'search_countries/search.html',{
                'search_country':search_country,
                'name':name,
                'ISO':ISO,
                'TLD':TLD,
                'phone_prefix':phone_prefix,
                'Capital':Capital,
                'AltNames':AltNames,
                'Poblation':Poblation,
                'Region':Region,
                'Subregion':Subregion,
                'Coordinates':Coordinates,
                'Gentilicio':Gentilicio,
                'Superficie':Superficie,
                'Gini':Gini,
                'timezone':timezone,
                'borderlines':borderlines,
                'native_language':native_language,
                'codeX':codeX,
                'coin':coin,
                'oficial_language':oficial_language,
                'asociations':asociations,
                'flag':flag
            })
        except APIRequestException:
            return render(request, 'search_countries/search_error.html',{'search_country':search_country})