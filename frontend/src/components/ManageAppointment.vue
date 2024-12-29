<template>
  <div class="manage-appointment">
    <NavbarAppointment />
    <div class="container-fluid mt-5 pt-3">
      <div class="row">
        <!-- Triage Results -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3 fw-bold mt-1">Triage Results</h3>
          <div class="drop-zone" @dragover.prevent="dragOver" @drop="drop($event, 'triage')">
            <ul class="list-group">
              <li
                class="list-group-item fw-bold"
                v-for="(appointment, index) in triageResults"
                :key="index"
                draggable="true"
                @dragstart="dragStart($event, appointment, 'triage')"
              >
                {{ appointment.patient.first_name }} {{ appointment.patient.last_name }} - {{ appointment.severity }} Priority
              </li>
            </ul>
          </div>
        </div>

        <!-- Checked-In -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3 fw-bold mt-1">Checked-In</h3>
          <div class="drop-zone" @dragover.prevent="dragOver" @drop="drop($event, 'checked-in')">
            <ul class="list-group">
              <li
                class="list-group-item"
                v-for="(appointment, index) in checkedInResults"
                :key="index"
                :class="{
                  'high-severity': appointment.severity === 'high',
                  'medium-severity': appointment.severity === 'medium',
                  'low-severity': appointment.severity === 'low'
                }"
                draggable="true"
                @dragstart="dragStart($event, appointment, 'checked-in')"
              >
                {{ appointment.patient.first_name }} {{ appointment.patient.last_name }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Checked-Out -->
        <div class="col-4">
          <h3 class="text-center mb-3 fw-bold mt-1">Checked-Out</h3>
          <div class="drop-zone" @dragover.prevent="dragOver" @drop="drop($event, 'checked-out')">
            <ul class="list-group">
              <li
                class="list-group-item"
                v-for="(appointment, index) in checkedOutResults"
                :key="index"
                :class="{
                  'high-severity': appointment.severity === 'high',
                  'medium-severity': appointment.severity === 'medium',
                  'low-severity': appointment.severity === 'low'
                }"
              >
                {{ appointment.patient.first_name }} {{ appointment.patient.last_name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ref } from 'vue';
import { Modal } from 'bootstrap';
import NavbarAppointment from './NavbarAppointment.vue';
import axios from 'axios';

export default {
  name: 'ManageAppointment',
  components: {
    NavbarAppointment,
  },
  setup() {
    const triageResults = ref([]); // For Triage Results
    const checkedInResults = ref([]); // For Checked-In Results
    const checkedOutResults = ref([]); // For Checked-Out Results
    const hours = ref([]);
    const appointments = ref({});
    const selectedPatient = ref({});
    const draggedItem = ref(null);

    const openPatientModal = (patient) => {
      selectedPatient.value = patient;
      const modal = new Modal(document.getElementById('patientInfoModal'));
      modal.show();
    };

    return {
      triageResults,
      checkedInResults,
      checkedOutResults, // Declare this property
      hours,
      appointments,
      draggedItem,
      selectedPatient,
      openPatientModal,
    };
  },
  methods: {
  async fetchAppointments(state) {
    try {
      const response = await axios.get(`https://careconnected-backend-v1-0.onrender.com/api/appointments/${state}/`);
      if (state === 'triage') this.triageResults = response.data;
      else if (state === 'checked-in') this.checkedInResults = response.data;
      else if (state === 'checked-out') this.checkedOutResults = response.data;
      console.log("here is the triage", this.triageResults);
      console.log("here is the check in", this.checkedInResults);
      console.log("here is the Out result", this.checkedOutResults);
    } catch (error) {
      console.error(`Error fetching ${state} appointments:`, error);
    }
  },
  
  dragStart(event, appointment, currentState) {
  event.dataTransfer.setData('appointmentId', appointment.id);
  event.dataTransfer.setData('currentState', currentState);
  console.log("Dragged appointment:", appointment.id);
  console.log("Current state:", currentState);
    },
    async drop(event, newState) {
      const appointmentId = event.dataTransfer.getData('appointmentId');
      const currentState = event.dataTransfer.getData('currentState');

      if (currentState !== newState) {
        try {
          await axios.patch(`https://careconnected-backend-v1-0.onrender.com/api/appointments/${appointmentId}/state/`, {
            state: newState,
          });
          await this.fetchAppointments(currentState); // Refresh source column
          await this.fetchAppointments(newState);    // Refresh target column
        } catch (error) {
          console.error(`Error updating appointment state:`, error);
        }
      }
    }
  },
  mounted() {
  this.fetchAppointments('triage');
  this.fetchAppointments('checked-in');
  this.fetchAppointments('checked-out');
}

};
</script>

<style scoped>
/* Styles for the page layout */
.manage-appointment {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.container-fluid {
  flex: 1;
}

.row {
  height: 88vh; /* Set a fixed height for the content area */
}

/* Left Section: Triage Results */
.col-4 {
  overflow-y: auto; /* Enable independent scrolling */
  max-height: 100%; /* Ensure it uses the full available height */
}


/* Sticky Title */
h3 {
  position: sticky;
  top: 0;
  background-color: #ffffff; /* Optional: Match background color to avoid overlapping effect */
  z-index: 1; /* Ensure it stays on top of other elements */
  padding: 10px 0; /* Add padding for spacing */
}

/* Schedule */
.schedule {
  margin-top: 20px;
}

.time-slot {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
}

.time-label {
  width: 100px;
  font-weight: bold;
  flex-shrink: 0;
}

.patient-list {
  flex-grow: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.list-group-item {
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #948aee;
  /* color: white; */
  /* color: black; */
  font: bold;
  display: flex;
  cursor: move;
  margin: 5px;
  min-height:40px;
  align-items: center;
  justify-content: space-between;
}

.drop-zone {
  min-height: 100px; /* Ensure space for dropping */
  height: 78vh;
  /*border: 2px dashed #007bff;  Visualize drop area */
  padding: 10px;
  background-color: white; /* Optional: Light background for drop zones */
}

.drop-zone:hover {
   background-color: #eaedeb; /* Highlight on hover */
}

.schedule-item {
  width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
  transition: background-color 0.3s ease;
}
/* color of the card for overview */
.high-severity {
  background-color: #f8d7da; /* Light Red */
  color: #721c24; /* Dark Red */
  border: 1px solid #f5c6cb;
}

.medium-severity {
  background-color: #fff3cd; /* Light Yellow */
  color: #856404; /* Dark Yellow */
  border: 1px solid #ffeeba;
}

.low-severity {
  background-color: #d4edda; /* Light Green */
  color: #155724; /* Dark Green */
  border: 1px solid #c3e6cb;
}





/* Modal Custom Styling */
.modal-content {
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); /* Shadow for depth */
  border: none; /* Remove default border */
}

/* Make the modal header background stand out */
.modal-header {
  background-color: #f8f9fa; /* Light grey background */
  border-bottom: 2px solid #e9ecef; /* Slight border for separation */
}

/* Customize the close button */
.btn-close {
  font-size: 1.2rem; /* Make the X larger */
  color: #333; /* Darker color for visibility */
  font-weight: bold; /* Bolder text */
  opacity: 1; /* Fully opaque */
}

.btn-close:hover {
  color: #ff3e3e; /* Red on hover for prominence */
  transform: scale(1.1); /* Slight scaling effect */
}
</style>
