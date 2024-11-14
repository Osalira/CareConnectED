<template>
  <div class="manage-appointment">
    <NavbarAppointment />
    <div class="container-fluid mt-5 pt-3">
      <div class="row">
        <!-- Left Section: Triage Result -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3 fw-bold mt-1">Triage Results</h3>
          <ul class="list-group">
            <li class="list-group-item" v-for="(patient, index) in triageResults" :key="index">
              {{ patient.name }} - {{ patient.severity }} Priority
            </li>
          </ul>
        </div>
        <!-- Right Section: Schedule with Dynamic Hours and Drag-and-Drop -->
        <div class="col-8">
          <h3 class="text-center mb-3 fw-bold mt-1">Schedule</h3>
          <div class="schedule">
            <div v-for="hour in hours" :key="hour" class="time-slot d-flex align-items-center border-bottom"
              @dragover.prevent="dragOver" @drop="drop($event, hour)">
              <div class="time-label">{{ hour }}:00 - {{ (hour + 1) % 24 }}:00</div>
              <div
                v-for="(patient, index) in appointments[hour] || []"
                :key="index"
                class="list-group-item schedule-item"
                :class="{
                  'high-severity': patient.severity === 'High',
                  'medium-severity': patient.severity === 'Medium',
                  'low-severity': patient.severity === 'Low'
                }"
                :title="patient.name"
                draggable="true"
                @dragstart="dragStart($event, patient)"
                @click="openPatientModal(patient)"
              >
                {{ patient.name }}
              </div>
         <!-- Patient Info Modal -->
            <div
              class="modal fade"
              id="patientInfoModal"
              tabindex="-1"
              aria-labelledby="patientInfoModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="patientInfoModalLabel">Patient Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <p><strong>Name:</strong> {{ selectedPatient.name }}</p>
                    <p><strong>Address:</strong> {{ selectedPatient.address }}</p>
                    <p><strong>Phone Number:</strong> {{ selectedPatient.phone_number }}</p>
                    <p><strong>Insurance:</strong> {{ selectedPatient.insurance }}</p>
                    <p><strong>Description:</strong> {{ selectedPatient.description }}</p>
                    <p><strong>Booking Time:</strong> {{ selectedPatient.created_at }}</p>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
    const triageResults = ref([]);
    const hours = ref([]);
    const appointments = ref({});
    const selectedPatient = ref({});

    // Reactive variables to hold the dragged item
    const draggedItem = ref(null);

    const openPatientModal = (patient) => {
      selectedPatient.value = patient;
      console.log("SelectedPatient value:", selectedPatient); //Debugging
      const modal = new Modal(document.getElementById('patientInfoModal'));
      modal.show();
    };

    return {
      triageResults,
      hours,
      appointments,
      draggedItem, // Track the item being dragged
      selectedPatient,
      openPatientModal
    };
  },
  methods: {
      async fetchTriageResults() {
        try {
          const response = await axios.get('http://localhost:8001/api/appointments/triage/');
          this.triageResults = response.data;
          console.log("Triage Results:", response.data); // Log to check structure
          this.populateAppointments();
        } catch (error) {
          console.error("Error fetching triage results:", error);
        }
      },
      calculateNext24Hours() {
        const currentHour = new Date().getHours();
        this.hours = Array.from({ length: 24 }, (_, i) => (currentHour + i) % 24);
      },
      populateAppointments() {
        this.appointments = {};
        let patientIndex = 0;

        this.hours.forEach((hour) => {
          this.appointments[hour] = this.triageResults.slice(patientIndex, patientIndex + 5).map((patient) => ({
            name: patient.name,
            id: patient.id || `${patient.name}-${hour}`,
            severity: patient.severity,
            phone_number: patient.phone_number,
            insurance: patient.insurance_number,
            description: patient.description,
            created_at : patient.created_at,
            list: hour,
          }));
          patientIndex += 5;
        });
        console.log("Appointments Object:", this.appointments);
      },

      dragStart(event, patient) {
          this.draggedItem = patient;  // Set the dragged item to the current patient
          console.log("Dragging Patient:", patient.name, "from Hour:", patient.list);  // Debugging
          event.dataTransfer.setData('text/plain', patient.id);
          event.dataTransfer.effectAllowed = 'move';
      },

      dragOver(event) {
        event.preventDefault(); // Allow the drop
      },
      drop(event, hour) {
          event.preventDefault();

          // Retrieve patient ID from the dataTransfer
          const itemId = event.dataTransfer.getData('text');
          const patient = this.draggedItem;  // Retrieve the current dragged item

          if (patient) {
            console.log("Dropping Patient:", patient.name, "to Hour:", hour);  // Debugging

            // Remove patient from the original hour list
            const originalSlot = this.appointments[patient.list];
            const originalIndex = originalSlot.findIndex(item => item.id === patient.id);

            if (originalIndex !== -1) {
              originalSlot.splice(originalIndex, 1);
              console.log("Removed from Hour:", patient.list);  // Debugging
            }

            // Add patient to the new hour slot and update the list property
            if (!this.appointments[hour]) {
              this.appointments[hour] = [];
            }
            patient.list = hour;  // Update the patient's list property to the new hour
            this.appointments[hour].push(patient);

            console.log("Added to Hour:", hour);  // Debugging

            // Clear the dragged item reference
            this.draggedItem = null;
          } else {
            console.log("No patient found to drop.");  // Debugging
          }
        }

    },
  mounted() {
    this.fetchTriageResults();
    this.calculateNext24Hours();

    // Update the hours every hour to keep the schedule accurate
    setInterval(() => {
      this.calculateNext24Hours();
    }, 3600000); // 3600000 ms = 1 hour
  },
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

/* Right Section: Schedule */
.col-8 {
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
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
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

/* Severity Styling */
.high-severity {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.medium-severity {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.low-severity {
  background-color: #d4edda;
  color: #155724;
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
