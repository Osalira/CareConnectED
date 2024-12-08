# appointments/models.py

from django.db import models
from django.utils.timezone import now

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    STATE_CHOICES = [
        ('triage', 'Triage'),
        ('checked-in', 'Checked In'),
        ('checked-out', 'Checked Out'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='triage')  # New field
    checked_in_time = models.DateTimeField(blank=True, null=True)  # Time when patient checked in
    checked_out_time = models.DateTimeField(blank=True, null=True)  # Time when patient checked out
    doctor_notes = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.state}"
