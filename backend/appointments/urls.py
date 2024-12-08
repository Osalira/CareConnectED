# appointments/urls.py

from django.urls import path
from .views import book_appointment, triage_appointments, search_appointments, appointment_history, update_appointment, appointments_by_state, update_appointment_state

from . import views
urlpatterns = [
    path('api/appointments/', book_appointment, name='book_appointment'),
    # path('api/appointments/triage/', triage_appointments, name='triage_appointments'),  # New endpoint
    path('api/appointments/search/', search_appointments, name='search_appointments'),
    path('api/appointments/history/', appointment_history, name='appointment_history'),
    path('api/appointments/today_count/', views.today_appointments_count, name='today_appointments_count'),
    path('api/appointments/current_schedule/', views.current_schedule, name='current_schedule'),
    path('api/appointments/recent_activity/', views.recent_activity, name='recent_activity'),
    path('api/appointments/<int:pk>/update/', views.update_appointment, name='update_appointment'),
    path('api/appointments/<str:state>/', appointments_by_state, name='appointments_by_state'),
    path('api/appointments/<int:pk>/state/', update_appointment_state, name='update_appointment_state'),
]


