<!-- src/components/BookAppointment.vue -->
<template>
    <div class="book-appointment ">
    <!-- Navbar -->
     <nav class="navbar navbar-expand-lg navbar-light bg-light ">
      <div class="container-fluid ">
        <!-- Logo Section -->
        <a class="navbar-brand" href="#">
          <img src="https://www.mistered.de/MisterEDk.png" alt="Logo" width="120" />
        </a>

        <!-- Right Side: Changed Mind question and Log out Button -->
        <div class="d-flex align-items-center ms-auto">
          <span class="fs-5 me-2 fw-bold">Changed your Mind?</span>
          <router-link to="/" class="btn  btn-primary ms-2">Log Out</router-link>
        </div>
      </div>
    </nav>
      <div class="container mb-3 ">
        <h2 class="text-center mb-4 mt-3">Appointment Details</h2>
        <form @submit.prevent="submitAppointment">
          <!-- Personal Information -->
          <div class="mb-2">
            <label for="name" class="form-label">Full Name</label>
            <input type="text" id="name" v-model="name" class="form-control" required placeholder="Enter your full name" />
          </div>
          
          <div class="mb-2">
            <label for="address" class="form-label">Address</label>
            <input type="text" id="address" v-model="address" class="form-control" required placeholder="Enter your address" />
          </div>
    
          <!-- Phone Number -->
          <div class="mb-2">
            <label for="phone" class="form-label">Phone Number</label>
            <input
              type="tel"
              id="phone"
              v-model="phoneNumber"
              class="form-control"
              required
              placeholder="Enter your phone number"
              pattern="^(\+?\d{1,3}[- ]?)?\d{10}$"
            />
            <small class="form-text text-muted">We will text you when your turn in the ER is ready.</small>
          </div>
  
          <!-- Health Insurance Number -->
          <div class="mb-2">
            <label for="insurance" class="form-label">Health Insurance Number</label>
            <input type="text" id="insurance" v-model="insuranceNumber" class="form-control" required placeholder="Enter your health insurance number" />
          </div>
    
          <!-- Optional Description -->
          <div class="mb-3">
            <label for="description" class="form-label">Description of Health Emergency <small>(Optional)</small></label>
            <textarea id="description" v-model="description" class="form-control" rows="4" placeholder="Briefly describe your health concern"></textarea>
          </div>
    
          <!-- Book Appointment Button -->
          <button type="submit" class="btn btn-primary w-100">Book Appointment</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  

  export default {
    data() {
      return {
        name: '',
        address: '',
        insuranceNumber: '',
        description: '',
      };
    },
    methods: {
      submitAppointment() {
        // Here you would send the data to your backend or display a success message
        alert(`Appointment booked for ${this.name}`);
        this.$router.push('/'); // Redirect to homepage or a confirmation page
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  </style>
  