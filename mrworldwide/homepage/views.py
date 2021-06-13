from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return redirect("search")
