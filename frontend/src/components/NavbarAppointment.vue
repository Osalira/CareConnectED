<template>
  <nav class="navbar bg-body-tertiary fixed-top">
    <div class="container-fluid">
      <!-- Page title as a clickable route -->
      <router-link :to="pageRoute" class="navbar-brand">{{ pageTitle }}</router-link>

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
          <button 
            v-for="(patient, index) in searchResults" 
            :key="index" 
            class="dropdown-item" 
            @click="selectPatient(patient)"
          >
            {{ patient.first_name }} {{ patient.last_name }}
          </button>
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
              <router-link class="nav-link active" to="/home-page" @click="closeOffcanvas">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/create-appointment" @click="closeOffcanvas">Create appointment</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/manage-appointment" @click="closeOffcanvas">Manage appointments</router-link>
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
import { ref, computed } from 'vue';
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

    const pageRoute = computed(() => {
      switch (pageTitle.value) {
        case 'Home':
          return '/home-page';
        case 'Create Appointment':
          return '/create-appointment';
        case 'Manage Appointments':
          return '/manage-appointment';
        case 'Edit Profile':
          return '/edit-profile';
        default:
          return '/home-page';
      }
    });

    const username = computed(() => authStore.user?.first_name || 'Guest');

    const logout = async () => {
      await authStore.logout(router);
    };

    const searchQuery = ref('');
    const searchResults = ref([]);
    const showDropdown = ref(false);

    const handleInput = debounce(async () => {
      if (searchQuery.value.length > 1) {
        try {
          const response = await axios.get(`http://localhost:8001/api/appointments/search?query=${searchQuery.value}`);
          searchResults.value = response.data;
          showDropdown.value = true;
        } catch (error) {
          console.error("Error fetching search results:", error);
          searchResults.value = [];
          showDropdown.value = false;
        }
      } else {
        searchResults.value = [];
        showDropdown.value = false;
      }
    }, 300);

    const selectPatient = (patient) => {
      searchQuery.value = '';
      searchResults.value = [];
      showDropdown.value = false;
      router.push({ name: 'SearchResults', query: { patientId: patient.id } });
    };

    const handleSearch = (event) => {
      if (searchResults.value.length) {
        selectPatient(searchResults.value[0]);
      }
    };

    const closeDropdown = () => {
      showDropdown.value = false;
    };

    const closeOffcanvas = () => {
      const offcanvasElement = document.getElementById('offcanvasNavbar');
      const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
      offcanvas.hide();
    };

    return {
      pageTitle,
      pageRoute,
      username,
      logout,
      searchQuery,
      searchResults,
      showDropdown,
      handleInput,
      selectPatient,
      handleSearch,
      closeDropdown,
      closeOffcanvas,
    };
  },
};
</script>

<style scoped>
/* Navbar container */
.navbar {
  background-color: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 10px 20px;
  font-family: Arial, sans-serif;
}

/* Navbar brand (page title) styling */
.navbar-brand {
  color: #050e18;
  font-size: 1.5rem;
  font-weight: bold;
  transition: color 0.3s;
}

.navbar-brand:hover {
  color: #0056b3;
  text-decoration: none;
}

/* Navbar items */
.navbar-nav .nav-link {
  color: #495057;
  font-weight: 500;
  transition: color 0.3s;
}

.navbar-nav .nav-link:hover {
  color: #007bff;
  text-decoration: none;
}

/* Active link styling */
.navbar-nav .nav-link.active {
  color: #4c5055;
  font-weight: bold;
}

/* Navbar toggler (for mobile view) */
.navbar-toggler {
  border: none;
  outline: none;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23495057' viewBox='0 0 30 30'%3E%3Cpath stroke='rgba(73, 80, 87, 0.7)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

/* Offcanvas menu styling */
.offcanvas {
  background-color: #ffffff;
  border-left: 1px solid #ddd;
}

.offcanvas-header {
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.offcanvas-body {
  padding-top: 20px;
}

.offcanvas .nav-item {
  margin-bottom: 10px;
}

/* Buttons and icons */
.btn-close {
  background-color: #e9ecef;
  border: none;
}

.btn-close:hover {
  background-color: #ced4da;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}

/* Search form styling */
.form-control {
  border-radius: 20px;
  border: 1px solid #ced4da;
  padding-left: 15px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: none;
}

/* Dropdown styling */
.dropdown-menu.show {
  max-height: 250px;
  overflow-y: auto;
  border: 1px solid #ddd;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  top: 100%;
  z-index: 1000;
}

.dropdown-item {
  padding: 10px 20px;
  color: #495057;
}

.dropdown-item:hover {
  background-color: #e9ecef;
}

.dropdown-item.text-muted {
  color: #6c757d;
  cursor: default;
}
</style>
