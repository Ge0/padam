import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  RedirectView)

from . import core
from .forms import BookingForm, JoinForm
from .models import Booking

logger = logging.getLogger(__name__)


class HomeView(ListView):
    template_name = 'booking/home.html'
    model = Booking

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingView(DetailView):
    template_name = 'booking/booking.html'
    model = Booking


class NewBookingView(CreateView):
    template_name = 'booking/new.html'
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking:list')

    def form_valid(self, form):
        cars = core.get_cars()
        if len(cars) == 0:
            messages.add_message(self.request, messages.ERROR,
                                 "There is not any car available.")
            return redirect(self.get_success_url())

        try:
            duration = core.get_duration(form.cleaned_data['start_address'],
                                         form.cleaned_data['dest_address'])
        except core.GetDurationError:
            messages.add_message(self.request, messages.ERROR,
                                 "Could not find a way from {} to {}.".format(
                                    form.cleaned_data['start_address'],
                                    form.cleaned_data['dest_address']))
            return super().form_invalid(form)
        else:
            booking = form.save(commit=False)
            booked_car = cars[0]
            booking.duration = duration
            booking.reservation_date = datetime.now()
            booking.user = self.request.user
            booking.duration = duration
            booking.state = True
            booking.car = booked_car
            core.set_car_disponibility(booked_car.id, False)
            return super().form_valid(form)


class JoinView(FormView):
    template_name = 'booking/join.html'
    form_class = JoinForm

    def form_valid(self, form):
        django_user = User.objects.create(
            username=form.cleaned_data['email'],
            last_name=form.cleaned_data['surname'],
            first_name=form.cleaned_data['firstname'],
            email=form.cleaned_data['email'])

        django_user.set_password(form.cleaned_data['password'])
        django_user.save()
        return redirect(reverse('login'))


class DeleteBookingView(RedirectView):
    pattern_name = "booking:list"

    def get_redirect_url(self, *args, **kwargs):
        try:
            core.delete_booking(kwargs['pk'])
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR,
                                 "Could not delete non-existing booking.")
        del kwargs['pk']
        return super().get_redirect_url(*args, **kwargs)
