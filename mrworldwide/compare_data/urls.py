from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.compare_choose_topic, name='compare_choose_topic'),
    url(r'^compare', views.compare, name='compare_index'),
]