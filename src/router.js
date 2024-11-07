// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import ManageAppointment from './components/ManageAppointment.vue';
import CreateAppointment from './components/CreateAppointment.vue';

const routes = [
  {
    path: '/',
    name: 'ManageAppointment',
    component: ManageAppointment,
  },
  {
    path: '/create-appointment',
    name: 'CreateAppointment',
    component: CreateAppointment,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
