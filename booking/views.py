from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .forms import BookingForm, JoinForm
from .models import Booking
from car.models import Car

import googlemaps
from datetime import datetime, timedelta

# Create your views here.

# Utils database functions

def get_cars():
	try:
		return Car.objects.filter(disponibility=True)
	except ObjectDoesNotExist:
		return None

def set_car_disponibility(id_car, state):
	try:
		car = Car.objects.get(id=id_car)
		car.disponibility = state
		car.save()
	except ObjectDoesNotExist:
		return None

def get_booking(id_booking):
	try:
		return Booking.objects.get(id=id_booking)
	except ObjectDoesNotExist:
		return None

def get_bookings(user_request):
	try:
		return Booking.objects.filter(user=user_request)
	except ObjectDoesNotExist:
		return None

def delete_booking(id_booking):
	try:
		inst = Booking.objects.get(id=id_booking)
		set_car_disponibility(inst.car.id, True)
		return inst.delete()
	except ObjectDoesNotExist:
		return None

# gmaps direction

def get_duration(start_address, dest_address):
	gmaps = googlemaps.Client(key='HARDCODED_KEY')
	now = datetime.now()
	try:
		directions_result = gmaps.directions(
			start_address,
			dest_address,
			mode="driving",
			departure_time=now)
		return directions_result[0]['legs'][0]['duration_in_traffic']['text']
	except googlemaps.exceptions.ApiError as inst:
		raise Http404(inst.args[0])

# Views functions

def home(request):
	data = get_bookings(request.user)
	return render(request,'booking/home.html', dict([("bookings", data)]))

def booking(request, bookingID):
	data = get_booking(bookingID)
	if data.user == request.user:
		return render(
			request,
			'booking/booking.html',
			dict([('booking', data)])
		)
	else:
		return HttpResponseForbidden()

def new(request):
	form = BookingForm(request.POST or None)
	if form.is_valid():
		booking = Booking()
		booking.user = request.user
		booking.reservation_date = datetime.now()
		booking.start_address = form.cleaned_data['start_address']
		booking.dest_address = form.cleaned_data['dest_address']
		booking.duration = get_duration(booking.start_address, booking.dest_address)
		booking.state = True
		if get_cars():
			booking.car = get_cars()[0]
			set_car_disponibility(get_cars()[0].id, False)
		booking.save()
		return redirect('/bookings/' + str(booking))

	return render(request, 'booking/new.html', locals())

def delete(request, bookingID):
	delete_booking(bookingID)
	data = get_bookings(request.user)

	return render(request,'booking/home.html', dict([("bookings", data)]))

def join(request):
	form = JoinForm(request.POST or None)
	if form.is_valid():
		userDjango = User.objects.create(
			username = form.cleaned_data['email'],
			last_name = form.cleaned_data['surname'],
			first_name = form.cleaned_data['firstname'],
			email = form.cleaned_data['email'])

		userDjango.set_password(request.POST['password'])
		userDjango.save()
		return redirect('/bookings/login')

	return render(request, 'booking/join.html', locals())
