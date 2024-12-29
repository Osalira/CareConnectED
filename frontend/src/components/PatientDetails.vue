<!-- <p>
    <strong>Patient Description:</strong> 
    <span v-if="appointment.description">
      "{{ appointment.description }}" 
    </span>
    <span v-else>N/A</span>
  </p> -->
  <template>
    <div class="patient-details">
      <NavbarAppointment />
      
      <!-- Title -->
      <div class="containerT mt-5">
        <h1 class="page-title text-center text-primary fw-bold">Patient History</h1>
      </div>
  
      <!-- Patient Info Section -->
      <div class="containerT mt-4">
        <div class="card shadow p-4 mb-4">
          <h2 class="text-secondary">{{ patientName }}</h2>
          <p><strong>Address:</strong> {{ patient.address }}</p>
          <p><strong>Phone Number:</strong> {{ patient.phone_number }}</p>
          <p><strong>Insurance Number:</strong> {{ patient.insurance_number }}</p>
        </div>
      </div>
  
      <!-- Appointment History Section -->
      <div class="containerT mt-4">
        <h2 class="text-primary text-center fw-bold">Appointment History</h2>
  
        <div v-if="appointments.length > 0" class="appointment-history mt-3">
          <div v-for="(appointment, index) in appointments" :key="index" class="card shadow mb-4 p-4">
            <h3 class="text-secondary">{{ formatDate(appointment.scheduled_time) }}</h3>
            <p><strong>Severity:</strong> {{ appointment.severity || 'N/A' }}</p>
            <p><strong>State:</strong> {{ appointment.state || 'N/A' }}</p>
            <p>
              <strong>Doctor Notes:</strong> 
              <span v-if="appointment.doctor_notes">
                "{{ appointment.doctor_notes }}" 
                <small class="text-muted">(by {{ appointment.doctor_name || 'Unknown Doctor' }})</small>
              </span>
              <span v-else>N/A</span>
            </p>
            <p><strong>Check-in Time:</strong> {{ formatDate(appointment.checked_in_time) }}</p>
            <p><strong>Check-out Time:</strong> {{ formatDate(appointment.checked_out_time) }}</p>
          </div>
        </div>
  
        <div v-else class="no-history text-center mt-5">
          <p class="text-muted">No appointment history found for this patient.</p>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import axios from "axios";
  import NavbarAppointment from "./NavbarAppointment.vue";
  
  export default {
    name: "PatientDetails",
    components: { NavbarAppointment },
    data() {
      return {
        patient: {},
        appointments: [],
        patientName: "",
      };
    },
    methods: {
      /**
       * Format the timestamp into a human-readable format
       * @param {String} timestamp
       * @returns {String} formatted date
       */
      formatDate(timestamp) {
        if (!timestamp) return "N/A";
        try {
          const date = new Date(timestamp);
          return date.toLocaleString("en-US", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            hour12: true,
          });
        } catch (error) {
          console.error("Error formatting date:", error);
          return timestamp;
        }
      },
    },
    async created() {
      const patientId = this.$route.params.patientId;
  
      try {
        // Fetch patient details and appointments
        const patientResponse = await axios.get(`https://careconnected-backend-v1-0.onrender.com/api/patient-records/${patientId}/`);
        this.patient = patientResponse.data.patient;
        this.appointments = patientResponse.data.appointments;
  
        // Set patient name for display
        this.patientName = `${this.patient.first_name} ${this.patient.last_name}`;
      } catch (error) {
        console.error("Error fetching patient details or appointments:", error);
      }
    },
  };
  </script>
  
  <style scoped>
  /* General styles */
  .patient-details {
    background-color: #f7f9fc;
    min-height: 100vh;
    padding-top: 20px;
  }
  
  .page-title {
    font-size: 2rem;
    font-weight: bold;
  }
  
  /* Card styles */
  .card {
    border-radius: 12px;
    border: 1px solid #ddd;
    background-color: #fff;
    max-width: 50%;
    width: auto;
    margin: 20px auto;
    
  }
  
  .card h2 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .card p {
    font-size: 1rem;
    margin-bottom: 10px;
  }
  
  /* No history message */
  .no-history {
    color: #6c757d;
    font-size: 1.2rem;
  }
  
  /* Appointment card styles */
  .appointment h3 {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .appointment p {
    font-size: 1rem;
  }
  </style>
  