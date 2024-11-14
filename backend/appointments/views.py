# appointments/views.py
from django.db.models import Q  # Import Q for complex queries
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from .serializers import AppointmentSerializer


@api_view(['POST'])
def book_appointment(request):
    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    # Fetch all appointments and sort by severity, then by booking time
    appointments = Appointment.objects.all().order_by('created_at')
    high_priority = [appt for appt in appointments if appt.severity == 'High']
    medium_priority = [appt for appt in appointments if appt.severity == 'Medium']
    low_priority = [appt for appt in appointments if appt.severity == 'Low']

    # Interleave patients to prevent starvation
    triage_order = []
    while high_priority or medium_priority or low_priority:
        triage_order.extend(high_priority[:5])
        high_priority = high_priority[5:]
        
        triage_order.extend(medium_priority[:3])
        medium_priority = medium_priority[3:]
        
        triage_order.extend(low_priority[:2])
        low_priority = low_priority[2:]

    # Prepare response data
    response_data = [
        {
            "name": f"{appt.first_name} {appt.last_name}",
            "severity": appt.severity,
            "address" : appt.address,
            "phone_number": appt.phone_number, 
            "insurance": appt.insurance_number,
            "description": appt.description,
            "created_at": appt.created_at.strftime('%Y-%m-%d %H:%M')
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

