"""Booking Django App core functions."""
import logging
from datetime import datetime

import googlemaps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Booking, Car

logger = logging.getLogger(__name__)


class GetDurationError(Exception):
    """Exception thrown when the get_duration helper fails at fetching
    a duration from google map API.
    """


def get_cars():
    try:
        return Car.objects.filter(disponibility=True)
    except ObjectDoesNotExist as exn:
        logger.warning("get_cars(): %s", str(exn))
        return None


def set_car_disponibility(id_car, state):
    try:
        car = Car.objects.get(id=id_car)
        car.disponibility = state
        car.save()
    except ObjectDoesNotExist as exn:
        logger.warning("set_car_disponibility(): %s", str(exn))
        return None


def get_booking(booking_id, queryset=None):
    try:
        if queryset is None:
            booking = Booking.objects.get(id=booking_id)
        else:
            booking = queryset.get(id=booking_id)
    except ObjectDoesNotExist as exn:
        logger.warning("get_booking(): %s", str(exn))
        return None
    else:
        return booking


def get_bookings(user_request):
    try:
        return Booking.objects.filter(user=user_request)
    except ObjectDoesNotExist as exn:
        logger.warning("get_bookings(): %s", str(exn))
        return None


def delete_booking(id_booking):
    try:
        inst = Booking.objects.get(id=id_booking)
    except ObjectDoesNotExist as exn:
        logger.warning("delete_booking(): %s", str(exn))
        raise exn
    else:
        set_car_disponibility(inst.car.id, True)
        return inst.delete()


def get_duration(start_address, dest_address):
    gmaps = googlemaps.Client(key=settings.GOOGLEMAP_KEY)
    now = datetime.now()
    try:
        directions_result = gmaps.directions(
            start_address, dest_address, mode="driving", departure_time=now)
        return directions_result[0]['legs'][0]['duration_in_traffic']['text']
    except (IndexError, googlemaps.exceptions.ApiError) as inst:
        logger.warning("get_duration(): %s", str(inst))
        raise GetDurationError(inst)
