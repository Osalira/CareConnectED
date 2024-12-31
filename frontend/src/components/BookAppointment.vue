<template>
    <div class="book-appointment">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <!-- Logo Section -->
          <a class="navbar-brand" href="#">
            <img src="/assets/logo1.jpeg" alt="Logo" width="120" />
          </a>
  
          <!-- Right Side: Changed Mind question and Log out Button -->
          <div class="d-flex align-items-center ms-auto">
            <span class="fs-5 me-2 fw-bold">Changed your Mind?</span>
            <router-link to="/" class="btn btn-primary ms-2">Log Out</router-link>
          </div>
        </div>
      </nav>
      <h2 class="text-center mb-4 mt-3">Appointment Details</h2>
      <div class="container mb-3">
        
        <form @submit.prevent="submitAppointment">
          <!-- Personal Information -->
          <!-- Personal Information -->
            <div class="row mb-2">
            <div class="col-md-6">
                <label for="firstName" class="form-label">First Name</label>
                <input type="text" id="firstName" v-model="firstName" class="form-control" required placeholder="Enter your first name" />
            </div>
            <div class="col-md-6">
                <label for="lastName" class="form-label">Last Name</label>
                <input type="text" id="lastName" v-model="lastName" class="form-control" required placeholder="Enter your last name" />
            </div>
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
  import Swal from 'sweetalert2';
  import { useSeverityStore } from '../store/severity';
  
  
  export default {
    setup() {
      const severityStore = useSeverityStore();
  
      return {
        // Use a computed property to make the severity level reactive
        severity: severityStore.severity,
      };
    },
    data() {
      return {
        firstName: '',
        lastName: '',
        address: '',
        phoneNumber: '',
        insuranceNumber: '',
        description: '',
      };
    },
    methods: {
      async submitAppointment() {
        try {
          const response = await this.$axios.post('/appointments/', {
              patient: {
                first_name: this.firstName,
                last_name: this.lastName,
                address: this.address,
                phone_number: this.phoneNumber,
                insurance_number: this.insuranceNumber,
              },
              description: this.description,
              severity: this.severity.toLowerCase(),
            });

          // console.log({
          //     first_name: this.firstName,
          //     last_name: this.lastName,
          //     address: this.address,
          //     phone_number: this.phoneNumber,
          //     insurance_number: this.insuranceNumber,
          //     description: this.description,
          //     severity: this.severity,
          //   });
          Swal.fire({
            title: `Appointment Booked!`,
            text: `${this.firstName} ${this.lastName}, you are put on the queue. You will receive a text with your scheduled appointment time about an hour before your appointment.`,
            icon: 'success',
            confirmButtonText: 'OK',
            background: '#d9f7ff', // Light blue background color
            color: '#333', // Dark text color for contrast
            confirmButtonColor: '#4CAF50', // Green color for confirm button
            iconColor: '#4CAF50', // Icon color to match the theme
            customClass: {
                popup: 'custom-swal-popup',
                title: 'custom-swal-title',
                content: 'custom-swal-content',
            },
            });
        //   this.$router.push('/'); // Redirect after successful submission
          setTimeout(() => {
            this.$router.push('/'); //Wait half a second before redirecting
          }, 3000);
        } catch (error) {
          console.error('Error booking appointment:', error);
        }
      },
    },
  };
  </script>
  
  
  <style scoped>
  .container {
    max-width: 600px;
  }

  /* Styling for the alert message */
  /* Optional additional styling */
    .custom-swal-popup {
    border-radius: 8px; /* Rounded corners */
    padding: 20px; /* Add padding */
    }

    .custom-swal-title {
    font-size: 1.5rem;
    color: #4CAF50; /* Green color for the title */
    }

    .custom-swal-content {
    font-size: 1rem;
    }

  </style>
  