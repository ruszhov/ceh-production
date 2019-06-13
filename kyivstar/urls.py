from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^calls/$', views.calls, name='calls'),
	url(r'^kyivstar/$', views.kyivstar, name='kyivstar'),
]