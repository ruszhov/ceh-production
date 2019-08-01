from django.conf.urls import url
from . import views

from django_filters.views import FilterView
from .filters import MaterialOrderFilter

urlpatterns = [
	url(r'^materialorder/$', views.materialorder, name='materialorder'),
	# url(r'^materialorder/results/$', views.search, name='materialordersearch'),
	# url(r'^materialorder/search/$', views.search, name="search"),
	# url(r'^materialorder/search/$', FilterView.as_view(filterset_class=MaterialOrderFilter,
 	#template_name='materialorder/search.html'), name='search'),
 	# url(r'^materialorder/search/$', views.search, name='search'),
	url(r'^materialorder/new/$', views.materialorder_new, name='materialorder_new'),
	# url(r'^materialorder/new/$', views.materialorder_new, name='materialorder_new'),
	url(r'^materialorder/(?P<pk>\d+)/edit/$', views.materialorder_edit, name='materialorder_edit'),
	url(r'^materialorder/(?P<pk>\d+)/status/$', views.paid_status, name='paid_status'),
]