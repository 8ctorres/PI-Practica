from django.conf.urls import url
from user_management import views

urlpatterns=[
    url(r'^login$', views.login_view),
	url(r'^logout$', views.logout_view),
	url(r'^signup$', views.signup_view),
]