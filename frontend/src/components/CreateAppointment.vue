<template>
    <div class="create-appointment">
      <NavbarAppointment />
      <div class="container-fluid mt-5 pt-3">
        <div class="row justify-content-center">
          <div class="col-6">
            <h3 class="text-center mb-3">Create Appointment</h3>
            <form @submit.prevent="createAppointment">
              <!-- First Name Input -->
              <div class="mb-3">
                <label for="firstName" class="form-label">First Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="firstName"
                  v-model="firstName"
                  placeholder="Enter first name"
                  required
                />
              </div>
  
              <!-- Last Name Input -->
              <div class="mb-3">
                <label for="lastName" class="form-label">Last Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="lastName"
                  v-model="lastName"
                  placeholder="Enter last name"
                  required
                />
              </div>
  
              <!-- Priority Dropdown -->
              <div class="mb-3">
                <label for="priority" class="form-label">Priority</label>
                <select
                  class="form-select"
                  id="priority"
                  v-model="priority"
                  required
                >
                  <option value="" disabled>Select priority</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>
  
              <!-- Time Block Selection -->
              <div class="mb-3">
                <label for="timeBlock" class="form-label">Time Block</label>
                <select
                  class="form-select"
                  id="timeBlock"
                  v-model="timeBlock"
                  required
                >
                  <option value="" disabled>Select time block</option>
                  <option value="00-1">00:00 - 01:00</option>
                  <option value="1-2">01:00 - 02:00</option>
                </select>
              </div>
  
              <!-- Buttons -->
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-primary">Create Appointment</button>
                <button type="button" class="btn btn-success" @click="scheduleAppointment">Schedule</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavbarAppointment from './NavbarAppointment.vue';
  
  export default {
    name: 'CreateAppointment',
    components: {
      NavbarAppointment,
    },
    data() {
      return {
        firstName: '',
        lastName: '',
        priority: '',
        timeBlock: '',
      };
    },
    methods: {
      createAppointment() {
        // Logic to handle appointment creation
        const appointment = {
          firstName: this.firstName,
          lastName: this.lastName,
          priority: this.priority,
          timeBlock: this.timeBlock,
        };
        console.log("Appointment Created:", appointment);
        // Reset the form fields after creation
        this.firstName = '';
        this.lastName = '';
        this.priority = '';
        this.timeBlock = '';
      },
      scheduleAppointment() {
        // Logic to handle scheduling of the appointment
        console.log("Scheduling Appointment:", {
          firstName: this.firstName,
          lastName: this.lastName,
          priority: this.priority,
          timeBlock: this.timeBlock,
        });
        // Add any additional scheduling functionality here
      },
    },
  };
  </script>
  
  <style scoped>
  .create-appointment {
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .container-fluid {
    flex: 1;
  }
  
  form {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  </style>
  