from twilio.rest import Client
from django.conf import settings

def send_sms_reminder(phone_number, message):
    # """Send SMS using Twilio."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )
