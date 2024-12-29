#backend\appointments\forms.py
from django import forms
from .models import Patient, Appointment

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'insurance_number']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'description', 'severity', 'scheduled_time', 'doctor_notes']

