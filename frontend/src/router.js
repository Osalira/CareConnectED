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
    meta: { guest: true },
  },
  {
    path: '/signin',
    name: 'SignInPage',
    component: SignInPage,
    meta: { guest: true },
  },
  {
    path: '/signup',
    name: 'SignUpPage',
    component: SignUpPage,
    meta: { guest: true },
  },
  {
    path: '/home-page',
    name: 'HomePage',
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/book-appointment',
    name: 'BookAppointment',
    component: BookAppointment,
    meta: { guest: true },
  },
  {
    path: '/manage-appointment',
    name: 'ManageAppointment',
    component: ManageAppointment,
    meta: { requiresAuth: true },
  },
  {
    path: '/create-appointment',
    name: 'CreateAppointment',
    component: CreateAppointment,
    meta: { requiresAuth: true },
  },
  {
    path: '/update-appointment',
    name: 'UpdateAppointment',
    component: UpdateAppointment,
    meta: { requiresAuth: true },
  },
  {
    path: '/records-history',
    name: 'RecordsHistory',
    component: RecordsHistory,
    meta: { requiresAuth: true },
  },
  {
    path: '/patients/:patientId/details',
    name: 'PatientDetails',
    component: PatientDetails,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'WelcomePage' });
  } else if (to.meta.guest && isAuthenticated) {
    next({ name: 'HomePage' });
  } else {
    next();
  }
});

export default router;
