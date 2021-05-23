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
            country_df = get_countries_by_name(search_country).iloc[0]
            country = country_df.to_dict()
            context = {"country": country}
            return render(request, 'search.html',context)
        except APIRequestException:
            return render(request, 'search_error.html',
                          {'search_country':search_country})
