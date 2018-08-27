from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^printstatistics/$', views.printstatistics, name='printstatistics'),
	url(r'^printstatistics/bbs/$', views.printstatistics_bbs, name='printstatistics_bbs'),
	url(r'^printstatistics/baner/$', views.printstatistics_baner, name='printstatistics_baner'),
	url(r'^printstatistics/oracal/$', views.printstatistics_oracal, name='printstatistics_oracal'),
	url(r'^printstatistics/holst/$', views.printstatistics_holst, name='printstatistics_holst'),
]