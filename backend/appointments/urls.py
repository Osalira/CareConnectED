# appointments/urls.py

from django.urls import path
from .views import book_appointment

urlpatterns = [
    path('api/appointments/', book_appointment, name='book_appointment'),
]
