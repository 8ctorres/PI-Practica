from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^profile/delete_chart$', views.delete_chart, name="delete_chart"),
	url(r'^profile$', views.profile_view, name="profile"),
    url(r'^login$', views.login_view, name="login"),
	url(r'^logout$', views.logout_view, name="logout"),
	url(r'^signup$', views.signup_view, name="signup"),
]