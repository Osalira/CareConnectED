// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import BookAppointment from './components/BookAppointment.vue';
import SignInPage from './components/SignInPage.vue';
import SignUpPage from './components/SignUpPage.vue';
import HomePage from './components/HomePage.vue';
import SearchResults from './components/SearchResults.vue';
import ManageAppointment from './components/ManageAppointment.vue';
import CreateAppointment from './components/CreateAppointment.vue';

const routes = [

  {
    path: '/',
    name: 'WelcomePage',
    component: WelcomePage,  // Default route is the welcome page
  },
  { path: '/book-appointment', 
    name: 'BookAppointment', 
    component: BookAppointment },
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
  {
    path:'/search-results',
    name: 'SearchResults',
    component: SearchResults,
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

