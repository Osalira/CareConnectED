<template>
  <div class="manage-appointment">
    <NavbarAppointment />
    <div class="container-fluid mt-5 pt-3">
      <div class="row">
        <!-- Left Section: Triage Result -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3">Triage Results</h3>
          <ul class="list-group">
            <li class="list-group-item" v-for="(patient, index) in triageResults" :key="index">
              {{ patient.name }} - {{ patient.severity }} Priority
            </li>
          </ul>
        </div>
        <!-- Right Section: Schedule with Dynamic Hours and Drag-and-Drop -->
        <div class="col-8">
          <h3 class="text-center mb-3">Schedule</h3>
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
              >
                {{ patient.name }}
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

    // Reactive variables to hold the dragged item
    const draggedItem = ref(null);

    return {
      triageResults,
      hours,
      appointments,
      draggedItem, // Track the item being dragged
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


/* time slot deco */
.schedule {
  margin-top: 20px;
}

.time-slot {
  display: flex; /* Use flexbox to align time label and patient list side by side */
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
}

.time-label {
  width: 100px; /* Fixed width to keep time labels aligned */
  font-weight: bold;
  flex-shrink: 0; /* Prevent time labels from shrinking */
}

.patient-list {
  flex-grow: 1; /* Allow patient list to take up remaining space */
  display: flex;
  flex-wrap: wrap; /* Wrap items to fit within the allotted space */
  gap: 5px; /* Space between items */
}

/* end of time slot style */
.list-group-item {
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
}

.list-group-item {
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
  transition: background-color 0.3s ease;
  
}

.schedule-item {
  width: 150px; /* Set a fixed width for uniform size */
  white-space: nowrap; /* Prevent text from wrapping */
  overflow: hidden; /* Hide overflow text */
  text-overflow: ellipsis; /* Show ellipsis (...) if text is too long */
  text-align: center; /* Center the text */
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
  transition: background-color 0.3s ease;
}
/* High Severity - Red Background */
.high-severity {
  background-color: #f8d7da; /* Light red */
  color: #721c24; /* Dark red text */
  border: 1px solid #f5c6cb;
}

/* Medium Severity - Yellow Background */
.medium-severity {
  background-color: #fff3cd; /* Light yellow */
  color: #856404; /* Dark yellow text */
  border: 1px solid #ffeeba;
}

/* Low Severity - Green Background */
.low-severity {
  background-color: #d4edda; /* Light green */
  color: #155724; /* Dark green text */
  border: 1px solid #c3e6cb;
}
</style>
