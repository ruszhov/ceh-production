from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logs/$', views.logs, name='logs'),
    url(r'^logs/rip/$', views.rip_logs, name='rip-logs'),
    url(r'^logs/print/$', views.print_logs, name='print-logs'),
    url(r'^logs/get-logs/$', views.get_logs, name='get-logs')
]