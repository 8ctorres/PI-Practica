from django.shortcuts import render
from datetime import datetime
from apis.worldbank import get_indicator_code, get_indicator_names
from apis.graphs import graph_1dataXcountries, graph_Xdata1country, graph_histograma
from apis.restcountries import get_all_names
import base64
import os
import traceback

# Create your views here.

indicators = get_indicator_names()
indicator_list = [indicators[indicator] for indicator in indicators]
country_list = get_all_names()

def graphs_index(request):
    return render(request, 'graphs/graph_index.html')

def graphs_1dataXcountries(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_1dataXcountries.html', context)

def graphs_Xdata1country(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_Xdata1country.html', context)

def graphs_histogram(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_histogram.html', context)

def graphs_histogram_result(request):
    return render(request, 'graphs/graph_histogram_result.html')

def graphs_1dataXcountries_result(request):
    return render(request, 'graphs/graph_1dataXcountries_result.html')

def graphs_Xdata1country_result(request):
    return render(request, 'graphs/graph_Xdata1country_result.html')