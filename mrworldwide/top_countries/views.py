from django.shortcuts import render

# Create your views here.

def top(request):
    return render(request, 'top_countries/top.html')