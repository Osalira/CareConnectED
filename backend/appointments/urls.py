# appointments/urls.py

from django.urls import path
from .views import book_appointment, triage_appointments  # Import the new triage view

urlpatterns = [
    path('api/appointments/', book_appointment, name='book_appointment'),
    path('api/appointments/triage/', triage_appointments, name='triage_appointments'),  # New endpoint
]
