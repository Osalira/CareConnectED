// src/router.js

import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import BookAppointment from './components/BookAppointment.vue';
import SignInPage from './components/SignInPage.vue';
import SignUpPage from './components/SignUpPage.vue';
import HomePage from './components/HomePage.vue';
import ManageAppointment from './components/ManageAppointment.vue';
import CreateAppointment from './components/CreateAppointment.vue';
import UpdateAppointment from './components/UpdateAppointment.vue';
import RecordsHistory from './components/RecordsHistory.vue';
import PatientDetails from './components/PatientDetails.vue';
import { useAuthStore } from './store/auth';

const routes = [
  {
    path: '/',
    name: 'WelcomePage',
    component: WelcomePage,
    meta: { guest: true }, // Accessible by guests
  },
  {
    path: '/signin',
    name: 'SignInPage',
    component: SignInPage,
    meta: { guest: true }, // Accessible by guests
  },
  {
    path: '/signup',
    name: 'SignUpPage',
    component: SignUpPage,
    meta: { guest: true }, // Accessible by guests
  },
  {
    path: '/book-appointment',
    name: 'BookAppointment',
    component: BookAppointment,
    meta: { public: true }, // Accessible by anyone
  },
  {
    path: '/home-page',
    name: 'HomePage',
    component: HomePage,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
  {
    path: '/manage-appointment',
    name: 'ManageAppointment',
    component: ManageAppointment,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
  {
    path: '/create-appointment',
    name: 'CreateAppointment',
    component: CreateAppointment,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
  {
    path: '/update-appointment',
    name: 'UpdateAppointment',
    component: UpdateAppointment,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
  {
    path: '/records-history',
    name: 'RecordsHistory',
    component: RecordsHistory,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
  {
    path: '/patients/:patientId/details',
    name: 'PatientDetails',
    component: PatientDetails,
    meta: { requiresAuth: true }, // Accessible by authenticated employees
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
// router.beforeEach(async (to, from, next) => {
//   const authStore = useAuthStore();
//   const isAuthenticated = authStore.isAuthenticated;

//   // If accessing a protected route
//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next({ name: 'WelcomePage', query: { redirect: to.fullPath } });
//   }
//   // If accessing a guest route while authenticated
//   else if (to.meta.guest && isAuthenticated) {
//     next({ name: 'HomePage' });
//   }
//   // If accessing a public route
//   else if (to.meta.public) {
//     next();
//   }
//   // Default behavior
//   else {
//     next();
//   }
// });

export default router;
