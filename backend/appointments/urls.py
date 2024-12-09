# appointments/urls.py

from django.urls import path
from .views import (
    book_appointment,
    search_appointments,
    reschedule_appointment,
    update_appointment,
    appointments_by_state,
    update_appointment_state,
    add_doctor_notes,
    appointments_last_24_hours,
    patient_records,
    patient_detail_with_appointments,
    patient_records_nav_search,
    today_overview, recent_activity, current_schedule,
)
from .views import appointments_last_24_hours
urlpatterns = [
    # Endpoint to book a new appointment
    path('api/appointments/', book_appointment, name='book_appointment'),
    
    # Endpoint to search appointments by patient name
    path('api/appointments/search/', search_appointments, name='search_appointments'),
    
    # Endpoint to update an appointment's details by ID
    path('api/appointments/<int:pk>/update/', update_appointment, name='update_appointment'),
    
    # Endpoint to retrieve appointments filtered by state (e.g., 'triage', 'checked-in', etc.)
    path('api/appointments/<str:state>/', appointments_by_state, name='appointments_by_state'),
    
    # Endpoint to update the state of an appointment (e.g., 'checked-in', 'checked-out') by ID
    path('api/appointments/<int:appointment_id>/state/', update_appointment_state, name='update_appointment_state'),
    
    # Endpoint to reschedule an appointment
    path('api/appointments/<int:appointment_id>/reschedule/', reschedule_appointment, name='reschedule_appointment'),
    
    # Endpoint to add doctor notes to an appointment
    path('api/appointments/<int:appointment_id>/doctor-notes/', add_doctor_notes, name='add_doctor_notes'),

    path('api/appointments-last-24-hours/', appointments_last_24_hours, name='appointments_last_24_hours'),
    # Endpoint to get all patient records
    path('api/patient-records/', patient_records, name='patient_records'),
    # Endpoint to get all the appointments of a patient
    path('api/patient-records/<int:patient_id>/', patient_detail_with_appointments, name='patient_detail_with_appointments'),
    # Endpointsnavbar search of patient records
    path('api/patient_records_nav_search/', patient_records_nav_search, name='patient_records_nav_search'),
    # homepage Endpoint
    path('api/appointments/today-overview', today_overview, name='today_overview'),
    path('api/appointments/recent-activity', recent_activity, name='recent_activity'),
    path('api/appointments/current-schedule', current_schedule, name='current_schedule'),
]



