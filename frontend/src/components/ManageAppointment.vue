<template>
    <div class="manage-appointment">
      <NavbarAppointment />
      <div class="container-fluid mt-5 pt-3">
        <div class="row">
          <!-- Left Section: Triage Result -->
          <div class="col-6 border-end">
            <h3 class="text-center mb-3">Triage Results</h3>
            <ul class="list-group">
              <li class="list-group-item" v-for="(result, index) in triageResults" :key="index">
                {{ result }}
              </li>
            </ul>
          </div>
  
          <!-- Right Section: Schedule -->
          <div class="col-6">
            <h3 class="text-center mb-3">Schedule</h3>
            <div class="schedule">
              <div v-for="hour in hours" :key="hour" class="time-slot d-flex align-items-center border-bottom">
                <div class="time-label">{{ hour }}:00 - {{ hour + 1 }}:00</div>
                <input
                  type="text"
                  class="form-control ms-3"
                  placeholder="Enter name"
                  v-model="appointments[hour]"
                />
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
    name: 'ManageAppointment',
    components: {
        NavbarAppointment,
    },
    data() {
      return {
        triageResults: ['Patient A - High Priority', 'Patient B - Medium Priority', 'Patient C - Low Priority'],
        hours: Array.from({ length: 24 }, (_, i) => i), // Array [0, 1, ..., 23]
        appointments: {}, // Track names entered for each hour slot
      };
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
  
  .time-slot {
    padding: 10px;
    display: flex;
  }
  
  .time-label {
    width: 100px;
    font-weight: bold;
  }
  </style>
  