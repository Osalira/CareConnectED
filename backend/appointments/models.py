#backend\appointments\models.py
from django.db import models
from django.utils.timezone import now
from twilio.rest import Client
from django.conf import settings
from datetime import timedelta
from celery import shared_task


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
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='triage')
    checked_in_time = models.DateTimeField(blank=True, null=True)
    checked_out_time = models.DateTimeField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    scheduled_time = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.state}"
    
    # er_capacity = 10
    # def calculate_waiting_time(self, er_capacity):
    #     """Calculate estimated waiting time based on ER capacity."""
    #     triage_count = Appointment.objects.filter(state='triage').count()
    #     checked_in_count = Appointment.objects.filter(state='checked-in').count()
    #     total_patients = triage_count + checked_in_count

    #     # Estimated waiting time in hours
    #     estimated_time = total_patients / er_capacity

    #     if estimated_time < 1:
    #         return 1
    #     elif 1 <= estimated_time < 2:
    #         return 2
    #     elif 2 <= estimated_time < 3:
    #         return 3
    #     else:
    #         return 4

    # def notify_patient(self, er_capacity):
    #     """Notify patient with estimated waiting time and schedule reminder."""
    #     from appointments.tasks import send_sms_reminder_task  # Import the task lazily to avoid circular import

    #     estimated_time = self.calculate_waiting_time(er_capacity)

    #     # Initial SMS notification
    #     send_sms_reminder_task.delay(
    #         self.patient.phone_number,
    #         f"Thank you for booking an appointment. Your estimated waiting time is {estimated_time} hours."
    #     )

    #     # Schedule reminder 30 minutes before the estimated time
    #     from datetime import timedelta
    #     reminder_time = now() + timedelta(hours=estimated_time - 0.5)
    #     send_sms_reminder_task.apply_async(
    #         args=[self.patient.phone_number, "We are ready to see you in 30 minutes."],
    #         eta=reminder_time
    #     )

