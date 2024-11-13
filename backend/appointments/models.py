# appointments/models.py

from django.db import models

class Appointment(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.first_name} {self.last_name} on {self.created_at}"
