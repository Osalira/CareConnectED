#backend\appointments\serializers.py

from rest_framework import serializers
from .models import Appointment, Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'address', 'phone_number', 'insurance_number']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()  # Nested serializer for patient

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'description', 'severity', 'scheduled_time', 'doctor_notes','doctor_name', 'checked_in_time', 'checked_out_time', 'state']

    def create(self, validated_data):
        # Extract patient data and create or get the patient instance
        patient_data = validated_data.pop('patient')
        patient, created = Patient.objects.get_or_create(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            address=patient_data['address'],
            phone_number=patient_data['phone_number'],
            insurance_number=patient_data['insurance_number'],
        )
        # Create the appointment
        return Appointment.objects.create(patient=patient, **validated_data)

