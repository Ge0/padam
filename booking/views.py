import logging
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from . import core
from .forms import BookingForm, JoinForm
from .models import Booking

logger = logging.getLogger(__name__)


def home(request):
    data = core.get_bookings(request.user)
    return render(request, 'booking/home.html', dict([("bookings", data)]))


def booking(request, bookingID):
    data = core.get_booking(bookingID)
    if data.user == request.user:
        return render(request, 'booking/booking.html',
                      dict([('booking', data)]))
    else:
        return HttpResponseForbidden()


def new(request):
    cars = core.get_cars()
    if len(cars) == 0:
        logger.warning("There is not any car available.")
        return redirect('/bookings/home')

    form = BookingForm(request.POST or None)
    if form.is_valid():

        try:
            duration = core.get_duration(form.cleaned_data['start_address'],
                                         form.cleaned_data['dest_address'])
        except core.GetDurationError:
            return render(request, 'booking/new.html', locals())
        else:
            booking = Booking()
            booking.user = request.user
            booking.reservation_date = datetime.now()
            booking.start_address = form.cleaned_data['start_address']
            booking.dest_address = form.cleaned_data['dest_address']
            booking.duration = duration
            booking.state = True
            booking.car = cars[0]
            core.set_car_disponibility(cars[0].id, False)
            booking.save()
            return redirect('/bookings/' + str(booking))

    return render(request, 'booking/new.html', locals())


def delete(request, bookingID):
    core.delete_booking(bookingID)
    data = core.get_bookings(request.user)

    return render(request, 'booking/home.html', dict([("bookings", data)]))


def join(request):
    form = JoinForm(request.POST or None)
    if form.is_valid():
        userDjango = User.objects.create(
            username=form.cleaned_data['email'],
            last_name=form.cleaned_data['surname'],
            first_name=form.cleaned_data['firstname'],
            email=form.cleaned_data['email'])

        userDjango.set_password(request.POST['password'])
        userDjango.save()
        return redirect(reverse('login'))

    return render(request, 'booking/join.html', locals())
