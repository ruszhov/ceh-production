from django.conf.urls import url
from . import views
from printorder.views import AddCommentView, DeleteCommentView, UpdateCommentView

urlpatterns = [
	url(r'^$', views.home, name='home'),
	# url(r'^$', views.OrdersListView.as_view(), name='home'),
	url(r'^order/(?P<pk>\d+)/edit/$', views.order_edit, name='order_edit'),
	url(r'^status/(?P<pk>\d+)/edit/$', views.status_edit, name='status_edit'),
    url(r'^description/(?P<pk>\d+)/edit/$', views.description_edit, name='description_edit'),
    url(r'^donesteps/add/$', AddCommentView.as_view(), name="done_steps"),
	url(r'^donesteps/remove/$', DeleteCommentView.as_view(), name="remove_comment"),
	url(r'^donesteps/edit/$', UpdateCommentView.as_view(), name="edit_comment"),
	# url(r'^description/(?P<pk>\d+)/edit/$', views.multiple_forms, name='description_edit'),
    # url(r'^orders/(?P<pk>\d+)/$', views.orders, name='orders'),
    # url(r'^orders/(?P<pk>\d+)/$', views.orders, name='orders'),
    url(r'^new/$', views.new_order, name='new_order'),
    url(r'^new/campaign/$', views.new_campaign, name='new_campaign'),    
    # url(r'^check_print_status/$', views.check_print_status, name='check_print_status'),
    # url(r'^status_check/$', views.status_check, name='status_check'),
]