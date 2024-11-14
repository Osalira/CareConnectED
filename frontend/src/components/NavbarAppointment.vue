<template>
  <nav class="navbar bg-body-tertiary fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">{{ pageTitle }}</a>

      <!-- Centered search bar with autocomplete dropdown -->
      <form class="d-flex mx-auto position-relative" @submit.prevent="handleSearch" v-click-outside="closeDropdown">
        <input 
          v-model="searchQuery" 
          @input="handleInput" 
          class="form-control me-2" 
          type="search" 
          placeholder="Search patient by name" 
          aria-label="Search"
          aria-expanded="true"
        />
        
        <!-- Show dropdown only if there's a search query -->
        <div 
          v-if="showDropdown && searchQuery.length > 1" 
          class="dropdown-menu show position-absolute w-100" 
          style="top: 100%;"
          aria-live="polite"
        >
          <!-- Display patient names if there are search results -->
          <button 
            v-for="(patient, index) in searchResults" 
            :key="index" 
            class="dropdown-item" 
            @click="selectPatient(patient)"
          >
            {{ patient.first_name }} {{ patient.last_name }}
          </button>
          <!-- Show "No Match Found" only if there are no search results -->
          <div v-if="searchResults.length === 0" class="dropdown-item text-muted">
            No Match Found
          </div>
        </div>
      </form>

      <h5 class="offcanvas-title ms-auto me-3 fw-bold" id="offcanvasNavbarLabel">{{ username }}</h5>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title fw-bold" id="offcanvasNavbarLabel">{{ username }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
            <li class="nav-item">
              <router-link class="nav-link active" to="/home-page">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/create-appointment">Create appointment</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/manage-appointment">Manage appointments</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import axios from 'axios';
import { debounce } from 'lodash';

export default {
  name: 'NavbarAppointment',
  directives: {
    clickOutside: {
      beforeMount(el, binding) {
        el.clickOutsideEvent = (event) => {
          // Check if the click was outside the element and its children
          if (!(el === event.target || el.contains(event.target))) {
            binding.value();
          }
        };
        document.addEventListener('click', el.clickOutsideEvent);
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent);
      },
    },
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    const pageTitle = computed(() => {
      switch (route.name) {
        case 'HomePage':
          return 'Home';
        case 'CreateAppointment':
          return 'Create Appointment';
        case 'ManageAppointment':
          return 'Manage Appointments';
        case 'EditProfile':
          return 'Edit Profile';
        default:
          return 'Home';
      }
    });

    const username = computed(() => authStore.user?.first_name || 'Guest');

    const logout = async () => {
      await authStore.logout(router);
    };

    // Search functionality
    const searchQuery = ref('');
    const searchResults = ref([]);
    const showDropdown = ref(false); // Controls visibility of the dropdown

    // Debounced search function integrated directly into handleInput
    const handleInput = debounce(async () => {
      if (searchQuery.value.length > 1) {
        try {
          const response = await axios.get(`http://localhost:8001/api/appointments/search?query=${searchQuery.value}`);
          searchResults.value = response.data;
          showDropdown.value = true; // Show dropdown when results are available
        } catch (error) {
          console.error("Error fetching search results:", error);
          searchResults.value = []; // Clear results on error
          showDropdown.value = false; // Hide dropdown on error
        }
      } else {
        searchResults.value = [];  // Clear results when input is empty
        showDropdown.value = false;
      }
    }, 300);

    const selectPatient = (patient) => {
      searchQuery.value = ''; // Clear the search input
      searchResults.value = [];
      showDropdown.value = false; // Hide the dropdown
      // Navigate to SearchResults page with patient ID as a query parameter
      router.push({ name: 'SearchResults', query: { patientId: patient.id } });
    };

    const handleSearch = (event) => {
      if (searchResults.value.length) {
        selectPatient(searchResults.value[0]);
      }
    };

    const closeDropdown = () => {
      showDropdown.value = false; // Close dropdown when clicking outside
    };

    return {
      pageTitle,
      username,
      logout,
      searchQuery,
      searchResults,
      showDropdown,
      handleInput,
      selectPatient,
      handleSearch,
      closeDropdown,
    };
  },
};
</script>

<style scoped>
/* Custom styling for the dropdown */
.dropdown-menu.show {
  max-height: 250px;
  overflow-y: auto;
  border: 1px solid #ddd;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  top: 100%; /* Ensures dropdown is below the input */
}

.dropdown-item.text-muted {
  color: #6c757d; /* Muted gray text for 'No Match Found' */
  cursor: default;
}
</style>
