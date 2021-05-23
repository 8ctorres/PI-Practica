from django.http.request import QueryDict
from django.shortcuts import render
from django.http import HttpResponse
from apis.restcountries import get_countries_by_name
from apis.exceptions import APIRequestException

# Create your views here.
def search_countries(request):
    if request.method == 'GET':
        try:
            search_country = request.GET['search_country'] or redirected_country
            country_df = get_countries_by_name(search_country).iloc[0]
            country = country_df.to_dict()
            context = {"country": country}
        except APIRequestException:
            context = {"error": "Invalid country"}
        except:
            context = {"error": "Unexpected error"}
        return render(request, 'search_countries/search.html',context)
