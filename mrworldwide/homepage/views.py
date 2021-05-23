from django.shortcuts import render
from django.http import HttpResponse
from apis.restcountries import get_countries_by_name

# Create your views here.
def homepage(request):
    country_df = get_countries_by_name("Spain").iloc[0]
    country = country_df.to_dict()
    context = {"country": country}
    return render(request, 'homepage/home.html',context)