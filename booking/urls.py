from django.conf.urls import url

from . import views

app_name = "booking"
urlpatterns = [
    url(r'^join$', views.JoinView.as_view(), name='join'),
    url(r'^home$', views.HomeView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', views.BookingView.as_view(), name='view'),
    url(r'^new$', views.NewBookingView.as_view(), name='new'),
    url(r'^delete/(?P<pk>\d+)$', views.DeleteBookingView.as_view(),
        name='delete'),
]
