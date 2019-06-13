from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^printstatistics/$', views.printstatistics, name='printstatistics'),
	url(r'^printstatistics/bbs/$', views.printstatistics_bbs, name='printstatistics_bbs'),
	url(r'^printstatistics/baner-lam/$', views.printstatistics_baner_lam, name='printstatistics_baner_lam'),
	url(r'^printstatistics/baner-lyt/$', views.printstatistics_baner_lyt, name='printstatistics_baner_lyt'),
	url(r'^printstatistics/baner-sitka/$', views.printstatistics_baner_sitka, name='printstatistics_baner_sitka'),
	url(r'^printstatistics/beklit/$', views.printstatistics_beklit, name='printstatistics_beklit'),
	url(r'^printstatistics/oracal-gl/$', views.printstatistics_oracal_gl, name='printstatistics_oracal_gl'),
	url(r'^printstatistics/oracal-mat/$', views.printstatistics_oracal_mat, name='printstatistics_oracal_mat'),
	url(r'^printstatistics/scroll/$', views.printstatistics_scroll, name='printstatistics_scroll'),
	url(r'^printstatistics/sitik/$', views.printstatistics_sitik, name='printstatistics_sitik'),
	url(r'^printstatistics/photo/$', views.printstatistics_photo, name='printstatistics_photo'),
	url(r'^printstatistics/holst/$', views.printstatistics_holst, name='printstatistics_holst'),
]