from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^profile$', views.profile_view, name="profile"),
    url(r'^login$', views.login_view, name="login"),
	url(r'^logout$', views.logout_view, name="logout"),
	url(r'^signup$', views.signup_view, name="signup"),
]