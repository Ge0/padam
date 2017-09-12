from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_address', 'dest_address']

    start_address = forms.CharField(max_length=250, label="Adresse de départ")
    dest_address = forms.CharField(
        max_length=250, label="Adresse de destination")


class JoinForm(forms.Form):
    surname = forms.CharField(max_length=50, label='Nom')
    firstname = forms.CharField(max_length=50, label='Prénom')
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        max_length=15, widget=forms.PasswordInput, label='Mot de passe')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'username'}))
    password = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'name': 'password'}))
