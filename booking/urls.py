from django.conf.urls import url

from . import views

app_name = "booking"
urlpatterns = [
    url(r'^join$', views.join, name='join'),
    url(r'^home$', views.home, name='list'),
    url(r'^(?P<booking_id>\d+)$', views.booking, name='view'),
    url(r'^new$', views.new, name='new'),
    url(r'^delete/(?P<booking_id>\d+)$', views.delete, name='delete'),
]
