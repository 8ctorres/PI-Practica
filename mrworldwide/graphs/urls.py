from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.graphs_index, name='graph_index'),
    url(r'^1dataXcountries', views.graphs_1dataXcountries, name='1dataXcountries_base'),
    url(r'^2data1countries', views.graphs_2data1country, name='2data1country_base'),
    url(r'^histogram', views.graphs_histogram, name='histogram_base'),
    
]