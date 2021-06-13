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
            # Si el usuario escribe más 3 letras, se busca por nombre porque no hay países
            # de menos de 4 letras, y si no, por código, que puede ser ISO-3 o ISO-2
            if len(search_country) > 3:
                country_df = get_countries_by_name(search_country).iloc[0]
            else:
                country_df = get_country_by_code(search_country).iloc[0]
            country = country_df.to_dict()
            # Si el país no tiene fronteras se añade N/A a la lista para que sea lo único
            # que aparece en la plantilla
            if len(country["borders"]) == 0:
                country["borders"] = "N/A"
            context = {"country": country, "country_code": country_df.name, 'country_list':country_list}
            return render(request, 'search_countries/search.html',context)
        except APIRequestException:
            context = {"error": "Invalid country"}
            return render(request, 'search_countries/search.html',context, status=404)
        except:
            context = {"error": "Unexpected error"}
            return render(request, 'search_countries/search.html',context, status=500)
