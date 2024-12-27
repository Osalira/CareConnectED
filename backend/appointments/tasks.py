# backend/appointments/tasks.py

from celery import shared_task
from .utils import send_sms_reminder

@shared_task
def send_sms_reminder_task(phone_number, message):
    # """Task to send an SMS reminder."""
    send_sms_reminder(phone_number, message)
