from django.shortcuts import render

# Create your views here.

def compare(request):
    return render(request, 'compare_data/compare.html')