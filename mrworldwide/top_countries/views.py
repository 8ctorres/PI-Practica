from django.shortcuts import render

# Create your views here.

def top(request):
    if request.method == 'GET':
        return render(request, 'top_countries/top.html')
    elif request.method == 'POST':
        context = {'data': 123}
        return render(request, 'top_countries/top.html', context)