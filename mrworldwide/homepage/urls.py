from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage-base'),
    path('comparacion/', views.comparacion, name='homepage-comparacion'),
]