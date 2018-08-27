from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	# url(r'^$', views.OrdersListView.as_view(), name='home'),
	url(r'^order/(?P<pk>\d+)/edit/$', views.order_edit, name='order_edit'),
	url(r'^status/(?P<pk>\d+)/edit/$', views.status_edit, name='status_edit'),
	url(r'^description/(?P<pk>\d+)/edit/$', views.description_edit, name='description_edit'),
    # url(r'^orders/(?P<pk>\d+)/$', views.orders, name='orders'),
    # url(r'^orders/(?P<pk>\d+)/$', views.orders, name='orders'),
    url(r'^new/$', views.new_order, name='new_order'),
    url(r'^new/campaign/$', views.new_campaign, name='new_campaign'),    
]