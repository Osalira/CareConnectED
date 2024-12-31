# backend/appointments/views.py
from django.db.models import Q  # Import Q for complex queries
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Appointment, Patient
from .serializers import AppointmentSerializer, PatientSerializer
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.functions import Lower
from appointments.tasks import send_sms_reminder_task  #
import math
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated users to register
def book_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        # Save the appointment
        appointment = serializer.save()

        # Calculate estimated waiting time ( adjust the ER capacity dynamically)
        ER_CAPACITY = 15  # Example capacity
        triage_count = Appointment.objects.filter(state='triage').count()
        checked_in_count = Appointment.objects.filter(state='checked-in').count()
        total_patients = triage_count + checked_in_count
        estimated_time = math.ceil(max(1, min(4, total_patients / ER_CAPACITY)))

        # Send initial SMS notification
        message = f"Thank you for booking an appointment. Your estimated waiting time is {estimated_time} hours."
        send_sms_reminder_task.delay(appointment.patient.phone_number, message)

        # Schedule reminder for 30 minutes before the estimated time
        reminder_time = now() + timedelta(hours=estimated_time - 0.5)
        send_sms_reminder_task.apply_async(
            args=[appointment.patient.phone_number, "We are ready to see you in 30 minutes."],
            eta=reminder_time
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Serializer errors:", serializer.errors)  # Log detailed errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# new 
@api_view(['POST'])
def update_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    # Update fields
    appointment.doctor_notes = request.data.get('doctor_notes', appointment.doctor_notes)
    appointment.scheduled_time = request.data.get('scheduled_time', appointment.scheduled_time)
    appointment.save()

    return Response(AppointmentSerializer(appointment).data)

@api_view(['GET'])
def appointments_by_state(request, state):
    # Fetch appointments based on state
    appointments = Appointment.objects.filter(state=state).order_by('created_at')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_appointment_state(request, pk):
    # Update state and optionally set times
    try:
        appointment = Appointment.objects.get(pk=pk)
        new_state = request.data.get('state')
        if new_state == 'checked-in':
            appointment.state = 'checked-in'
            appointment.checked_in_time = now()
        elif new_state == 'checked-out':
            appointment.state = 'checked-out'
            appointment.checked_out_time = now()
        else:
            return Response({"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

        appointment.save()
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    

# Update appointmetn state, the patient checked in/ checked out, what time?
@api_view(['PATCH'])
def update_appointment_state(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_state = request.data.get('state')

    if new_state == 'checked-in':
        appointment.state = 'checked-in'
        appointment.checked_in_time = now()
    elif new_state == 'checked-out':
        appointment.state = 'checked-out'
        appointment.checked_out_time = now()
    elif new_state == 'triage':
        appointment.state = 'triage'
        appointment.checked_in_time = None
        appointment.checked_out_time = None
    else:
        return Response({"error": "Invalid state provided."}, status=400)

    appointment.save()
    return Response(AppointmentSerializer(appointment).data, status=200)

@api_view(['PATCH'])
def add_doctor_notes(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    notes = request.data.get('doctor_notes')
    doctor_name = request.data.get('doctor_name')

    if not notes or not doctor_name:
        return Response({"error": "Doctor notes and name are required."}, status=400)

    appointment.doctor_notes = notes
    appointment.doctor_name = doctor_name
    appointment.save()

    return Response(AppointmentSerializer(appointment).data, status=200)

@api_view(['PATCH'])
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_time = request.data.get('scheduled_time')

    if not new_time:
        return Response({"error": "Scheduled time is required."}, status=400)

    appointment.scheduled_time = new_time
    appointment.save()
    return Response(AppointmentSerializer(appointment).data, status=200)

@api_view(['GET'])
def search_appointments(request):
    query = request.GET.get('name', '')
    appointments = Appointment.objects.filter(
        patient__first_name__icontains=query
    ) | Appointment.objects.filter(
        patient__last_name__icontains=query
    )
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=200)

def appointments_last_24_hours(request):
    # Calculate the time range
    last_24_hours = now() - timedelta(hours=24)
    appointments = Appointment.objects.filter(created_at__gte=last_24_hours)

    # Serialize the data
    data = [
        {
            "id": appointment.id,
            "first_name": appointment.patient.first_name,  # Access through the related patient
            "last_name": appointment.patient.last_name,   # Access through the related patient
            "description": appointment.description,
            "severity": appointment.severity,
            "state": appointment.state,
            "created_at": appointment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for appointment in appointments
    ]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def patient_records(request):
    try:
        # Retrieve all patients, sorted alphabetically by first and last name
        patients = Patient.objects.order_by(Lower('first_name'), Lower('last_name'))
        # Serialize the patient data
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def patient_detail_with_appointments(request, patient_id):
    try:
        # Get the patient by ID
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Serialize patient data
        patient_serializer = PatientSerializer(patient)

        # Get all appointments associated with the patient
        appointments = Appointment.objects.filter(patient=patient).order_by('-created_at')
        
        # Serialize appointment data
        appointment_serializer = AppointmentSerializer(appointments, many=True)

        # Combine both into a single response
        response_data = {
            "patient": patient_serializer.data,
            "appointments": appointment_serializer.data
        }

        return Response(response_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
# navbar search of patient records
@api_view(['GET'])
def patient_records_nav_search(request):
    try:
        # Get the search query parameter
        query = request.GET.get('query', '')
        # Retrieve all patients, sorted alphabetically
        patients = Patient.objects.order_by(Lower('first_name'), Lower('last_name'))
        
        if query:
            # Filter patients whose first or last name starts with the query (case-insensitive)
            patients = patients.filter(
                Q(first_name__istartswith=query) | Q(last_name__istartswith=query)
            )
        
        # Serialize the patient data
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def today_overview(request):
    """Fetch today's overview: Appointments and Pending Triage."""
    try:
        current_time = now()
        midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

        # Count appointments created since midnight
        appointments_count = Appointment.objects.filter(created_at__gte=midnight).count()

        # Count patients in the triage state created since midnight
        pending_triage_count = Appointment.objects.filter(
            state='triage', created_at__gte=midnight
        ).count()

        return Response({
            "appointments": appointments_count,
            "pending_triage": pending_triage_count
        }, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

           
           
@api_view(['GET'])
def recent_activity(request):
    """Fetch recent activity (last 10 bookings)."""
    try:
        recent_appointments = Appointment.objects.order_by('-created_at')[:10]

        # Build the response data
        recent_activity_data = [
            {
                "id": appt.id,
                "message": f"{appt.patient.first_name} {appt.patient.last_name} booked an appointment at {appt.created_at.strftime('%H:%M')}."
            }
            for appt in recent_appointments
        ]

        return Response({"recent_activity": recent_activity_data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def current_schedule(request):
    """Fetch all patients currently in the ER (checked-in)."""
    try:
        checked_in_appointments = Appointment.objects.filter(state='checked-in')

        # Build the response data
        schedule_data = [
            {
                "id": appt.id,
                "time": appt.scheduled_time.strftime('%H:%M'),
                "patientName": f"{appt.patient.first_name} {appt.patient.last_name}",
                "priority": appt.severity
            }
            for appt in checked_in_appointments
        ]

        return Response({"scheduled_patients": schedule_data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


