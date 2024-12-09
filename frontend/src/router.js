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

const routes = [

  {
    path: '/',
    name: 'WelcomePage',
    component: WelcomePage,  // Default route is the welcome page
  },
  { path: '/book-appointment', 
    name: 'BookAppointment', 
    component: BookAppointment 
  },
 
  {
    path: '/signin',
    name: 'SignInPage',
    component: SignInPage,  
  },
  {
    path: '/signup',
    name: 'SignUpPage', // Add route for SignUpPage
    component: SignUpPage,
  },
  { path: '/home-page', name: 'HomePage', component: HomePage },
  { path: '/manage-appointment', name: 'ManageAppointment', component: ManageAppointment },
  { path: '/create-appointment', name: 'CreateAppointment', component: CreateAppointment },
  { path: '/update-appointment', 
    name: 'UpdateAppointment', 
    component: UpdateAppointment 
  },
  {
    path: '/records-history',
    name: 'RecordsHistory',
    component: RecordsHistory,
  },
  { 
    path: '/patients/:patientId/details', 
    name: 'PatientDetails', 
    component: PatientDetails 
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

