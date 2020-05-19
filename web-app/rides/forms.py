from django import forms
from .models import Ride
from .models import Driver


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            'destination',
            'arrival',
            'number',
            'shared',
            'email',
            'user',
        ]



class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'plate',
            'type',
            'passengers'
        ]