from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    disponibility = models.BooleanField()

    def __str__(self):
        return str(self.id)


class Booking(models.Model):
    date = models.DateTimeField(
        auto_now_add=True, auto_now=False, verbose_name="Date de creation")
    reservation_date = models.DateTimeField(
        auto_now_add=False, auto_now=False, verbose_name="Date de réservation")
    car = models.OneToOneField(Car, related_name='car')
    user = models.ForeignKey(User, related_name='user')
    start_address = models.CharField(
        max_length=250, verbose_name="Adresse de départ")
    dest_address = models.CharField(
        max_length=250, verbose_name="Adresse de destination")
    state = models.BooleanField()
    duration = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)
