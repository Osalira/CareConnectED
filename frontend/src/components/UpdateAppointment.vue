<template>
    <div class="manage-appointments">
      <NavbarAppointment />
      <div class="mt-5 pt-3">
        <h1 class="fw-bold">Update Appointments</h1>
        <div class="search-section">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by name"
            class="search-input"
            @input="filterAppointments"
          />
        </div>
  
        <table class="appointments-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>State</th>
              <th>Severity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in filteredAppointments" :key="appointment.id">
              <td>
                {{ appointment.first_name }} {{ appointment.last_name }}
              </td>
              <td>{{ appointment.state }}</td>
              <td :class="severityClass(appointment.severity)">{{ appointment.severity }}</td>
              <td>
                <button
                  @click="markCheckedIn(appointment.id)"
                  :disabled="appointment.state === 'checked-in'"
                  class="action-button check-in-button"
                >
                  Check In
                </button>
                <button
                  @click="markCheckedOut(appointment.id)"
                  :disabled="appointment.state === 'checked-out'"
                  class="action-button check-out-button"
                >
                  Check Out
                </button>
                <button
                  @click="openRescheduleModal(appointment)"
                  class="action-button reschedule-button"
                >
                  Reschedule
                </button>
                <button
                  @click="openNotesModal(appointment)"
                  class="action-button notes-button"
                >
                  Add Notes
                </button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <RescheduleModal
          v-if="showRescheduleModal"
          :appointment="selectedAppointment"
          @close="closeRescheduleModal"
          @refresh="fetchAppointmentsLast24Hours"
        />
        <NotesModal
          v-if="showNotesModal"
          :appointment="selectedAppointment"
          @close="closeNotesModal"
          @refresh="fetchAppointmentsLast24Hours"
        />
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import NavbarAppointment from "./NavbarAppointment.vue";
  import RescheduleModal from "./RescheduleModal.vue";
  import NotesModal from "./NotesModal.vue";
  
  export default {
    components: { RescheduleModal, NotesModal, NavbarAppointment },
    data() {
      return {
        searchQuery: "",
        appointments: [],
        filteredAppointments: [],
        selectedAppointment: null,
        showRescheduleModal: false,
        showNotesModal: false,
      };
    },
    methods: {
      async fetchAppointmentsLast24Hours() {
        try {
          const response = await axios.get("https://backendcareconnected.onrender.com/api/appointments-last-24-hours/");
          this.appointments = response.data;
          this.filteredAppointments = response.data;
        } catch (error) {
          console.error("Error fetching appointments:", error);
        }
      },
      filterAppointments() {
        const query = this.searchQuery.toLowerCase();
        this.filteredAppointments = this.appointments.filter((appointment) =>
          `${appointment.first_name} ${appointment.last_name}`
            .toLowerCase()
            .startsWith(query)
        );
      },
      async markCheckedIn(id) {
        await axios.patch(`http://localhost:8001/api/appointments/${id}/state/`, { state: "checked-in" });
        this.fetchAppointmentsLast24Hours();
      },
      async markCheckedOut(id) {
        await axios.patch(`http://localhost:8001/api/appointments/${id}/state/`, { state: "checked-out" });
        this.fetchAppointmentsLast24Hours();
      },
      openRescheduleModal(appointment) {
        this.selectedAppointment = appointment;
        this.showRescheduleModal = true;
      },
      closeRescheduleModal() {
        this.showRescheduleModal = false;
      },
      openNotesModal(appointment) {
        this.selectedAppointment = appointment;
        this.showNotesModal = true;
      },
      closeNotesModal() {
        this.showNotesModal = false;
      },
      severityClass(severity) {
        if (severity === "High") return "high-severity";
        if (severity === "Medium") return "medium-severity";
        if (severity === "Low") return "low-severity";
        return "";
      },
    },
    mounted() {
      this.fetchAppointmentsLast24Hours();
    },
  };
  </script>
  
  <style scoped>
  .manage-appointments {
    max-width: 1200px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    /* overflow-y: auto; */
  }
  
  h1 {
    font-size: 1.8rem;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .search-section {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    
  }
  
  .search-input {
    width: 300px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    outline: none;
  }
  
  .search-button {
    padding: 10px 20px;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .search-button:hover {
    background-color: #0056b3;
  }
  
  .appointments-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .appointments-table th,
  .appointments-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  .appointments-table th {
    background-color: #f1f1f1;
    font-weight: bold;
    /* overflow-y: auto; */
  }

  .appointments-table thead{
    position: sticky;
  }

  .appointments-table tbody{
    overflow-y: auto;
  }
  .action-button {
    padding: 5px 10px;
    margin: 2px;
    border: none;
    border-radius: 4px;
    color: white;
    cursor: pointer;
    font-size: 0.9rem;
  }
  
  .check-in-button {
    background-color: #28a745;
  }
  
  .check-in-button:hover {
    background-color: #218838;
  }
  
  .check-out-button {
    background-color: #dc3545;
  }
  
  .check-out-button:hover {
    background-color: #c82333;
  }
  
  .reschedule-button {
    background-color: #ffc107;
    color: black;
  }
  
  .reschedule-button:hover {
    background-color: #e0a800;
  }
  
  .notes-button {
    background-color: #17a2b8;
  }
  
  .notes-button:hover {
    background-color: #138496;
  }
  
  /* Severity Classes */
  .high-severity {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .medium-severity {
    background-color: #fff3cd;
    color: #856404;
  }
  
  .low-severity {
    background-color: #d4edda;
    color: #155724;
  }
  /* some c table */
  /* Ensure body and html have fixed height */
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden; /* Prevent scrollbar on the body */
  display: flex;
  flex-direction: column;
}
.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table thead {
  position: sticky;
  top: 0;
  background-color: #f1f1f1; /* Header background */
  z-index: 1;
}

.appointments-table tbody {
  /* display: block; */
  max-height: 600px; /* Set desired height for the scrollable body */
  overflow-y: auto;
}

.appointments-table tr {
  /* display: table; */
  width: 100%;
  table-layout: fixed; /* Ensures columns align correctly */
}

.appointments-table th,
.appointments-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

.appointments-table th {
  font-weight: bold;
}

  </style>
  