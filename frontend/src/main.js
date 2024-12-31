// src/main.js

import { createApp } from 'vue';
import pinia from './store'; // Import the configured Pinia instance
import router from './router'; // Import Vue Router
import App from './App.vue';

// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import * as bootstrap from 'bootstrap';
window.bootstrap = bootstrap;

// Import Axios instance
import axiosInstance from '@/utils/axiosInstance.js';

// Import the authentication store
import { useAuthStore } from './store/auth';

(async () => {
    try {
        // Initialize the app
        const app = createApp(App);

        // Make Axios globally available
        app.config.globalProperties.$axios = axiosInstance;

        // Register the 'click-outside' directive
        app.directive('click-outside', {
            beforeMount(el, binding) {
                el.clickOutsideEvent = (event) => {
                    if (!(el === event.target || el.contains(event.target))) {
                        binding.value(event); // Invoke the callback provided in the directive
                    }
                };
                document.addEventListener('click', el.clickOutsideEvent);
            },
            unmounted(el) {
                document.removeEventListener('click', el.clickOutsideEvent);
            },
        });

        // Use Pinia for state management
        app.use(pinia);

        // Use Vue Router
        app.use(router);

        // Initialize the auth store
        const authStore = useAuthStore();

        // Attempt to refresh the access token
        await authStore.refreshAccessToken();

        if (authStore.accessToken) {
            await authStore.fetchUser();
        }

        // Mount the app to the DOM
        app.mount('#app');
    } catch (error) {
        console.error('Failed to initialize the application:', error);
        // Optionally, handle initialization failure (e.g., redirect to an error page or show a message)
    }
})();
