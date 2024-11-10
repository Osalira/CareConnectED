<template>
    <div class="home-page">
      <NavbarAppointment />
  
      <div class="container mt-5">
        <div class="row">
          
          <!-- Left Column: Overview and Recent Activity -->
          <div class="col-md-6">
            
            <!-- Today's Overview -->
            <div class="overview mb-3">
              <h3>Today's Overview</h3>
              <ul>
                <li>Appointments: {{ todayAppointments.length }}</li>
                <li>Pending Triage: {{ pendingTriage.length }}</li>
              </ul>
              <!-- Create Appointment Button -->
              <router-link to="/create-appointment" class="btn btn-primary mt-3">Create Appointment</router-link>
            </div>
  
            <!-- Recent Activity -->
            <div class="recent-activity mt-4">
              <h3>Recent Activity</h3>
              <ul>
                <li v-for="activity in recentActivity" :key="activity.id">{{ activity.message }}</li>
              </ul>
            </div>
            
          </div>
  
          <!-- Right Column: Today's Schedule -->
          <div class="col-md-6">
            <div class="schedule">
              <h3>Today's Schedule</h3>
              <div v-for="appointment in todayAppointments" :key="appointment.id" class="appointment-item mb-2">
                <p><strong>{{ appointment.time }}</strong> - {{ appointment.patientName }} (Priority: {{ appointment.priority }})</p>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavbarAppointment from './NavbarAppointment.vue';
  
  export default {
    name: 'HomePage',
    components: {
      NavbarAppointment,
    },
    data() {
      return {
        todayAppointments: [
          { id: 1, patientName: 'John Doe', time: '10:00', priority: 'High' },
          { id: 2, patientName: 'Jane Smith', time: '11:00', priority: 'Medium' },
        ],
        pendingTriage: [{ id: 3, patientName: 'Alice Jones' }],
        recentActivity: [
          { id: 1, message: 'Appointment created for John Doe at 10:00' },
          { id: 2, message: 'Triage completed for Alice Jones' },
        ],
      };
    },
  };
  </script>
  
  <style>
  .home-page {
    padding: 20px;
  }
  
  .overview, .recent-activity, .schedule {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 5px;
  }
  
  .recent-activity {
    margin-top: 20px;
  }
  
  .appointment-item {
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }
  </style>
  