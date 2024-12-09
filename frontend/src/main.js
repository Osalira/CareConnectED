import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { useAuthStore } from './store/auth'
//
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import * as bootstrap from 'bootstrap';
window.bootstrap = bootstrap;

//import './style.css' // Replace with your custom styles if needed

const app = createApp(App)

// Click-outside directive
app.directive('click-outside', {
    beforeMount(el, binding) {
      el.clickOutsideEvent = (event) => {
        if (!(el === event.target || el.contains(event.target))) {
          binding.value(event); // Call the provided callback
        }
      };
      document.addEventListener('click', el.clickOutsideEvent);
    },
    unmounted(el) {
      document.removeEventListener('click', el.clickOutsideEvent);
    },
  });
// Set up Pinia for state management
app.use(createPinia())

// Set up Vue Router
app.use(router)

// Initialize the auth store and set CSRF token
const authStore = useAuthStore()
authStore.setCsrfToken()

// Mount the app to the #app element in index.html
app.mount('#app')
