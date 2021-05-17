from django.shortcuts import render

# Create your views here.

def graphs_index(request):
    return render(request, 'graphs/graph_index.html')

def graphs_1dataXcountries(request):
    return render(request, 'graphs/graph_index.html')

def graphs_2data1country(request):
    return render(request, 'graphs/graph_index.html')

def graphs_histogram(request):
    return render(request, 'graphs/graph_index.html')