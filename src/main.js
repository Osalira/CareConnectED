import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

// https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// createApp(App).mount('#app')

createApp(App)
  .use(router)
  .mount('#app');
