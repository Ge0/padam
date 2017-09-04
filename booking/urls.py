from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login$', auth_views.login, name='booking_login'),
    url(r'^logout$',
        auth_views.logout, {'next_page': 'booking_login'},
        name='booking_logout'),
    url(r'^join$', views.join, name='booking_join'),
    url(r'^home$', views.home, name='booking_list'),
    url(r'^(?P<bookingID>\d+)$', views.booking, name='booking'),
    url(r'^new$', views.new, name='booking_new'),
    url(r'^delete/(?P<bookingID>\d+)$', views.delete, name='booking_delete'),
]
