<template>
<div>
     <!-- Navbar -->
     <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Logo Section -->
        <a class="navbar-brand" href="#">
          <img src="https://www.mistered.de/MisterEDk.png" alt="Logo" width="120" />
        </a>

        <!-- Right Side: Staff Question and Sign In Button -->
        <div class="d-flex align-items-center ms-auto">
          <span class="fs-5 me-2 fw-bold">Are you a staff member?</span>
          <router-link to="/signin" class="btn btn-lg btn-primary ms-2">Sign In</router-link>
        </div>
      </div>
    </nav>
  <div class="container text-center my-5">
    <!-- Title -->
    <h1 class="display-3 mb-4">What's your Emergency?</h1>

    <!-- Emergency Categories -->
    <div class="row mb-4">
      <!-- High Emergency -->
      <div class="col-md-4 mb-4" @click="selectSeverity('High')">
        <div class="card h-100 border-danger">
          <div class="card-body">
            <h2 class="card-title text-danger">High</h2>
            <p class="card-text">
              Severe injuries or life-threatening conditions, such as chest pain, stroke symptoms, or major trauma. Immediate medical attention is required.
            </p>
          </div>
        </div>
      </div>

      <!-- Medium Emergency -->
      <div class="col-md-4 mb-4" @click="selectSeverity('Medium')">
        <div class="card h-100 border-warning">
          <div class="card-body">
            <h2 class="card-title text-warning">Medium</h2>
            <p class="card-text">
              Urgent medical concerns, like high fever, fractures, or breathing difficulties. Requires medical attention within a few hours.
            </p>
          </div>
        </div>
      </div>

      <!-- Low Emergency -->
      <div class="col-md-4 mb-4" @click="selectSeverity('Low')">
        <div class="card h-100 border-success">
          <div class="card-body">
            <h2 class="card-title text-success">Low</h2>
            <p class="card-text">
              Non-life-threatening issues, such as minor cuts, cold symptoms, or mild aches. Medical attention can be delayed or handled by a primary care physician.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Dropdown and Book Appointment Button -->
     <div class="d-flex flex-column align-items-center">
          <div class="col-md-6 col-lg-4">
          <div class="mb-4 ">
          <label for="severity" class="form-label">Select Emergency Severity</label>
          <select
            id="severity"
            class="form-select"
            v-model="selectedSeverity"
            @change="onDropdownSelect"
          >
            <option value="" disabled>Select severity level...</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          </div>

          <button
            class="btn btn-primary buttonSize"
            :disabled="!selectedSeverity"
            @click="bookAppointment"
          >
            Book Appointment
          </button>
          </div>
     </div>

  </div>
</div>
</template>

<script>

export default {
  data() {
    return {
      selectedSeverity: "" // Stores the selected severity level
    };
  },
  methods: {
    // Set the selectedSeverity based on the card clicked
    selectSeverity(level) {
      this.selectedSeverity = level;
    },
    // Book appointment function (can navigate or show confirmation)
    // bookAppointment() {
    //   alert(`Appointment booked with ${this.selectedSeverity} severity`);
    // },
    bookAppointment() {
    this.$router.push('/book-appointment');
    },
    onDropdownSelect() {
      // This method is optional and can be used if extra functionality is needed on dropdown selection
      console.log(`Dropdown selected: ${this.selectedSeverity}`);
    }
  }
};
</script>

<style scoped>
/* Center the cards and add spacing */
.card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

/* Center Book Appointment Button */
.buttonSize {
  max-width: 600px;
}

button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
/* navbar style */
/* .navbar {
  padding: 1rem;
} */

.container-fluid {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand img {
  max-height: 60px;
}

.d-flex {
  align-items: center;
}

</style>
