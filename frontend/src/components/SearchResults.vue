<template>
    <div class="search-results">
      <NavbarAppointment />
      
      <!-- Title -->
      <h1 class="page-title mt-4 pt-5 text-center">Patient History</h1>
      
      <!-- Patient Info Section -->
      <div class="patient-info card p-3 mb-4">
        <h2>{{ patientName }}</h2>
        <p><strong>Address:</strong> {{ patientAddress }}</p>
        <p><strong>Phone Number:</strong> {{ patientPhoneNumber }}</p>
        <p><strong>Insurance Number:</strong> {{ patientInsuranceNumber }}</p>
      </div>
  
      <!-- Appointment History Section -->
      <div v-if="appointments.length > 0" class="appointment-history">
        <div v-for="(appointment, index) in appointments" :key="index" class="appointment card mb-3 p-3">
          <h3 class="appointment-date">{{ formatDate(appointment.created_at) }}</h3>
          <p><strong>Description:</strong> {{ appointment.description }}</p>
          <p><strong>Severity:</strong> {{ appointment.severity }}</p>
        </div>
      </div>
      
      <div v-else class="no-history">
        <p>No appointment history found for this patient.</p>
      </div>
    </div>
  </template>
  
  

  <script>
import NavbarAppointment from './NavbarAppointment.vue';
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'SearchResults',
  components: {
    NavbarAppointment,
  },
  setup() {
    const route = useRoute();
    const patientId = ref(route.query.patientId); // Track patientId as a ref

    const patientName = ref('');
    const patientAddress = ref('');
    const patientPhoneNumber = ref('');
    const patientInsuranceNumber = ref('');
    const appointments = ref([]);

    const fetchPatientData = async () => {
      try {
        const response = await axios.get(`http://localhost:8001/api/appointments/history?patientId=${patientId.value}`);
        const data = response.data;

        if (data.length > 0) {
          // Set patient basic info (shown only once)
          patientName.value = `${data[0].first_name} ${data[0].last_name}`;
          patientAddress.value = data[0].address;
          patientPhoneNumber.value = data[0].phone_number;
          patientInsuranceNumber.value = data[0].insurance_number;

          // Set appointments data (only description and severity per appointment)
          appointments.value = data.map((appointment) => ({
            created_at: appointment.created_at,
            description: appointment.description,
            severity: appointment.severity,
          }));
        } else {
          patientName.value = 'No patient found';
          appointments.value = [];
        }
      } catch (error) {
        console.error('Error fetching patient data:', error);
      }
    };

    // Watch for changes in the patientId and refetch data if it changes
    watch(() => route.query.patientId, (newPatientId) => {
      patientId.value = newPatientId;
      fetchPatientData();
    });

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    onMounted(fetchPatientData);

    return {
      patientName,
      patientAddress,
      patientPhoneNumber,
      patientInsuranceNumber,
      appointments,
      formatDate,
    };
  },
};
</script>

  
  <style scoped>
  .search-results {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-title {
    font-size: 2rem;
    font-weight: bold;
    color: #4A4A4A;
    margin-bottom: 20px;
  }
  
  .patient-info {
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .patient-info h2 {
    font-size: 1.5rem;
    color: #333;
  }
  
  .patient-info p {
    margin: 0;
    color: #555;
    font-size: 1rem;
  }
  
  .appointment-history {
    margin-top: 20px;
  }
  
  .appointment {
    border: 1px solid #e3e6f0;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    background-color: #ffffff;
  }
  
  .appointment-date {
    font-size: 1.2rem;
    color: #6c757d;
    font-weight: bold;
  }
  
  .appointment p {
    font-size: 1rem;
    color: #333;
    margin: 5px 0;
  }
  
  .no-history {
    text-align: center;
    color: #6c757d;
    font-size: 1.2rem;
    margin-top: 20px;
  }
  </style>
  