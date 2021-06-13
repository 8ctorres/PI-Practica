from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.

# Como decidimos que la homepage sea un ejemplo del CU search
# la vista hace un redirect
def homepage(request):
    return redirect("search")
