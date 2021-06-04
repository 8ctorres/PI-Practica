from django.shortcuts import render

# Create your views here.

def graphs_index(request):
    return render(request, 'graphs/graph_index.html')

def graphs_1dataXcountries(request):
    return render(request, 'graphs/graph_1dataXcountries.html')

def graphs_2data1country(request):
    return render(request, 'graphs/graph_2data1country.html')

def graphs_histogram(request):
    return render(request, 'graphs/graph_histogram.html')

def graphs_histogram_result(request):
    return render(request, 'graphs/graph_histogram_result.html')

def graphs_1dataXcountries_result(request):
    return render(request, 'graphs/graph_1dataXcountries_result.html')

def graphs_2data1country_result(request):
    return render(request, 'graphs/graph_2data1country_result.html')