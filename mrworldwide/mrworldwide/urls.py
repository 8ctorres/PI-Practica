"""mrworldwide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
"""from apis.restcountries import get_all_countries
from search_countries.models import Pais

first_row = get_all_countries().values[0]

pais = Pais(first_row)
print(pais)"""
#print(f"Candidad de paises {Pais.objects.all()}")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('homepage.urls')),
    url(r'^compare_data/', include('compare_data.urls')),
    url(r'^top/', include('top_countries.urls')),
    url(r'^graphs/', include('graphs.urls')),
    url(r'^search/', include('search_countries.urls')),
    url(r'^user/', include('user_management.urls'))
]
