from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'name',
            'address',
            'phone_number',
            'insurance_number',
            'description',
            'severity',
        ]
