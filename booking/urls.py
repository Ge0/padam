from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^join$', views.join, name='join'),
    url(r'^home$', views.home, name='list'),
    url(r'^(?P<bookingID>\d+)$', views.booking, name='view'),
    url(r'^new$', views.new, name='new'),
    url(r'^delete/(?P<bookingID>\d+)$', views.delete, name='delete'),
]
