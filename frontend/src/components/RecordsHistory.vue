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
  </template>
  
  <script>
  import axios from "axios";
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
          const response = await axios.get("https://careconnected-backend-v1-0.onrender.com/api/patient-records/");
          this.patients = response.data;
          console.log("patient dats", response.data);
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
  
  .records-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .records-table th,
  .records-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  .records-table th {
    background-color: #f1f1f1;
    font-weight: bold;
  }
  </style>
  