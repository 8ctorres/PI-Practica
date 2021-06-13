from django.shortcuts import render
from apis.restcountries import get_countries_by_name, get_country_by_code
from apis.exceptions import APIRequestException
from apis.restcountries import get_all_names

# Create your views here.
def search_countries(request):
    country_list = get_all_names()
    if request.method == 'GET':
        try:
            search_country = request.GET['search_country']
        except:
            search_country = "ESP"

        try:
            if len(search_country) > 3:
                country_df = get_countries_by_name(search_country).iloc[0]
            else:
                country_df = get_country_by_code(search_country).iloc[0]
            country = country_df.to_dict()
            context = {"country": country, "country_code": country_df.name, 'country_list':country_list}
        except APIRequestException:
            context = {"error": "Invalid country"}
        except:
            context = {"error": "Unexpected error"}
        return render(request, 'search_countries/search.html',context)
