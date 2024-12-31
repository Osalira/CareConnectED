<template>
  <div>
    <!-- Main Content with Emergency Cards on the Left and Sign In on the Right -->
    <div class="container my-5">
      <div class="row">
        <!-- Left Column: Emergency Categories and Dropdown -->
        <div class="col-md-8 pe-md-5 border-end">
          <h1 class="display-3 mb-1 text-center">What's your Emergency?</h1>
          <span class="fs-5 text-center d-block mt-1 mb-5">Book an Appointment Below</span>
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
          <div class="d-flex flex-column align-items-center mb-4">
            <label for="severity" class="form-label">Select Emergency Severity</label>
            <select
              id="severity"
              class="form-select w-50"
              v-model="severityStore.severity"
              @change="onDropdownSelect"
            >
              <!-- <option value="" disabled>Select severity level...</option> -->
              <option value="" >Select severity level...</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
            <button
              class="btn btn-primary mt-3"
              :disabled="!severityStore.severity"
              @click="bookAppointment"
            >
              Book Appointment
            </button>
          </div>
        </div>

        <!-- Right Column: Centered Sign In for Staff Members -->
        <div class="col-md-4 d-flex justify-content-center align-items-center">
          <div class="w-75">
            <span class="fs-4 fw-bold text-center">Sign In For Staff Members</span>
            <div class="adjusted-margin">
              <SignInPage />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    <!-- Footer Section -->
    <footer class="text-center py-3 mt-5 border-top">
      <p>Made by Ben Osalira</p>
      <a href="https://www.benosalira.com/" target="_blank"
      rel="noopener noreferrer" class="text-primary">
        Contact Info
      </a>
    </footer>
</template>

<script>
import SignInPage from './SignInPage.vue';
import { useSeverityStore } from '@/store/severity';

export default {
  components: {
    SignInPage,
  },
  setup() {
    const severityStore = useSeverityStore();

    function selectSeverity(level) {
      severityStore.setSeverity(level);
    }

    function bookAppointment() {
      // severityStore.severity && this.$router.push('/book-appointment');
      severityStore.severity;
      
    }

    function onDropdownSelect() {
      console.log(`Dropdown selected: ${severityStore.severity}`);
    }

    return { severityStore, selectSeverity, bookAppointment, onDropdownSelect };
  },
  methods: {
   
    bookAppointment() {
      
      this.$router.push('/book-appointment');

    },
    onDropdownSelect() {
      console.log(Dropdown, selected, useSeverityStore().severity);
    },
  },
};
</script>

<style scoped>
/* Card Hover Effect */
.card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.border-end {
  border-right: 2px solid #ddd;
  padding-right: 2rem;
}

.adjusted-margin {
  margin-top: -80px;
}

.display-3 {
  margin-bottom: 0.5rem;
}

.fs-5 {
  display: block;
  margin-top: 0;
}

footer {
  background-color: #f8f9fa;
  color: #6c757d;
  font-size: 0.9rem;

}
footer a {
  color: #007bff;
  text-decoration: none;
}
footer a:hover {
  text-decoration: underline;
}

</style>
