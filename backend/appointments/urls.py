# appointments/urls.py

from django.urls import path
from .views import book_appointment, triage_appointments, search_appointments, appointment_history  # Import the new triage view

urlpatterns = [
    path('api/appointments/', book_appointment, name='book_appointment'),
    path('api/appointments/triage/', triage_appointments, name='triage_appointments'),  # New endpoint
    path('api/appointments/search/', search_appointments, name='search_appointments'),
    path('api/appointments/history/', appointment_history, name='appointment_history'),
]
