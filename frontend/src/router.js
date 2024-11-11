// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import SignInPage from './components/SignInPage.vue';
import SignUpPage from './components/SignUpPage.vue';
import HomePage from './components/HomePage.vue';
import ManageAppointment from './components/ManageAppointment.vue';
import CreateAppointment from './components/CreateAppointment.vue';

const routes = [
  {
    path: '/signin',
    name: 'SignInPage',
    component: SignInPage,  // Default route is the sign-in page
  },
  {
    path: '/signup',
    name: 'SignUpPage', // Add route for SignUpPage
    component: SignUpPage,
  },
  { path: '/home-page', name: 'HomePage', component: HomePage },
  { path: '/manage-appointment', name: 'ManageAppointment', component: ManageAppointment },
  { path: '/create-appointment', name: 'CreateAppointment', component: CreateAppointment },
  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

