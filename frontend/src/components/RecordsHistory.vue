<template>
  <div class="records-history">
    <NavbarAppointment />
    <div class="mt-5 pt-3">
      <h1 class="fw-bold">Patient Records</h1>
      <div class="search-section">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by name"
          class="search-input"
          @input="filterPatients"
        />
      </div>

      <!-- Display loading indicator -->
      <div v-if="isLoading" class="text-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Display error message -->
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>

      <!-- Scrollable table container -->
      <div class="table-container">
        <table class="records-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Insurance Number</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="patient in filteredPatients" 
              :key="patient.id" 
              @click="navigateToPatientDetails(patient.id)"
              style="cursor: pointer"
            >
              <td>{{ patient.first_name }} {{ patient.last_name }}</td>
              <td>{{ patient.phone_number }}</td>
              <td>{{ patient.address }}</td>
              <td>{{ patient.insurance_number || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import NavbarAppointment from "./NavbarAppointment.vue";
  
  export default {
    name: "RecordsHistory",
    components: { NavbarAppointment },
    data() {
      return {
        searchQuery: "",
        patients: [],
        filteredPatients: [],
      };
    },
    methods: {
      async fetchPatientRecords() {
        try {
          const response = await this.$axios.get("/patient-records/");
          this.patients = response.data;
          // console.log("patient dats", response.data);
          this.filteredPatients = response.data; // Initially show all patients
        } catch (error) {
          console.error("Error fetching patient records:", error);
        }
      },
      filterPatients() {
        const query = this.searchQuery.toLowerCase();
        this.filteredPatients = this.patients.filter((patient) =>
            `${patient.first_name} ${patient.last_name}`.toLowerCase().includes(query) ||
            patient.phone_number.includes(query) ||
            patient.insurance_number?.toLowerCase().includes(query)
        );
        },
        navigateToPatientDetails(patientId) {
            console.log("patient ID:", patientId);
            this.$router.push({ name: 'PatientDetails', params: { patientId } });
        },
    },
    mounted() {
      this.fetchPatientRecords();
    },
  };
  </script>
  
  <style scoped>

/* fixed header and scrollable tbody */
.records-history {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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

/* Scrollable table container */
.table-container {
  max-height: 70vh; /* Adjust the height as needed */
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
}

.records-table th,
.records-table td {
  padding: 12px 15px;
  border: 1px solid #ddd;
  text-align: center;
  min-width: 150px; /* Ensure columns have a minimum width */
}

/* Fixed table header */
.records-table thead th {
  position: sticky;
  top: 0;
  background-color: #f1f1f1; /* Background color for header */
  z-index: 2; /* Ensure header stays above table body */
  box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.4); /* Optional: Add a subtle shadow */
}

/* Hover effect for table rows */
.records-table tbody tr:hover {
  background-color: #e9ecef;
  cursor: pointer;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }

  .records-table th,
  .records-table td {
    padding: 8px 10px;
    min-width: 100px;
  }
}

/* Error message styling */
.error {
  color: red;
  margin-top: 10px;
  font-size: 0.9rem;
}

.error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
}

.action:disabled {
  background: #aaa;
  cursor: not-allowed;
}
  /* Loading spinner */
.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Error message */
.alert {
  margin-top: 20px;
  text-align: center;
}

/* scrollbar style */
::-webkit-scrollbar{
    width: 10px;
}

::-webkit-scrollbar-track{
    background-color: #ddd;
}

::-webkit-scrollbar-thumb{
    background: linear-gradient( rgb(161, 161, 159),rgb(128, 128, 134));
}
</style>
  