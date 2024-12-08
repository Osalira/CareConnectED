# appointments/views.py
from django.db.models import Q  # Import Q for complex queries
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from .serializers import AppointmentSerializer
from django.utils.timezone import now


@api_view(['POST'])
def book_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Serializer errors:", serializer.errors)  # Log detailed errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def search_appointments(request):
    query = request.GET.get('query', '')
    appointments = Appointment.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def triage_appointments(request):
    # Fetch all appointments and sort by creation time
    appointments = Appointment.objects.all().order_by('created_at')

    # Separate appointments by severity
    high_priority = [appt for appt in appointments if appt.severity == 'high']
    medium_priority = [appt for appt in appointments if appt.severity == 'medium']
    low_priority = [appt for appt in appointments if appt.severity == 'low']

    # Interleave patients to prevent starvation
    triage_order = []
    while high_priority or medium_priority or low_priority:
        triage_order.extend(high_priority[:5])
        high_priority = high_priority[5:]

        triage_order.extend(medium_priority[:3])
        medium_priority = medium_priority[3:]

        triage_order.extend(low_priority[:2])
        low_priority = low_priority[2:]

    # Prepare response data using patient and appointment details
    response_data = [
        {
            "name": f"{appt.patient.first_name} {appt.patient.last_name}",
            "severity": appt.severity,
            "address": appt.patient.address,
            "phone_number": appt.patient.phone_number,
            "insurance": appt.patient.insurance_number,
            "description": appt.description,
            "created_at": appt.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        for appt in triage_order
    ]

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def appointment_history(request):
    patient_id = request.GET.get('patientId')
    appointments = Appointment.objects.filter(id=patient_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def today_appointments_count(request):
    now = timezone.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    appointments_count = Appointment.objects.filter(created_at__range=(midnight, now)).count()
    return Response({"count": appointments_count}, status=status.HTTP_200_OK)

@api_view(['GET'])
def current_schedule(request):
    now = timezone.now()
    two_hours_later = now + timedelta(hours=2)
    upcoming_appointments = Appointment.objects.filter(created_at__range=(now, two_hours_later)).order_by('created_at')[:10]
    response_data = [
        {
            "id": appt.id,
            "patientName": f"{appt.first_name} {appt.last_name}",
            "time": appt.created_at.strftime('%H:%M'),
            "priority": appt.severity
        }
        for appt in upcoming_appointments
    ]
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recent_activity(request):
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:7]
    response_data = [
        {
            "id": appt.id,
            "message": f"Appointment created for {appt.first_name} {appt.last_name} at {appt.created_at.strftime('%H:%M')}"
        }
        for appt in recent_appointments
    ]
    return Response(response_data, status=status.HTTP_200_OK)

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