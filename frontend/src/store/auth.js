// src/store/auth.js

import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axiosInstance';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
        accessToken: null, // Stored in memory
    }),
    actions: {
        async login(employee_id, password) {
            try {
                const response = await axiosInstance.post('/login/', {
                    employee_id,
                    password,
                });

                if (response.data.success) {
                    this.user = response.data.user;
                    this.isAuthenticated = true;
                    this.accessToken = response.data.access;
                    console.log('Login successful:', this.user);
                    router.push({ name: 'HomePage' });
                } else {
                    this.isAuthenticated = false;
                    this.user = null;
                    this.accessToken = null;
                    console.error('Login failed:', response.data.message);
                }
            } catch (error) {
                console.error('Error during login:', error.response?.data || error.message);
                this.isAuthenticated = false;
                this.user = null;
                this.accessToken = null;
                throw error;
            }
        },

        async logout() {
            try {
                await axiosInstance.post('/employees/logout/');
            } catch (error) {
                console.error('Error during logout:', error.response?.data || error.message);
                // Proceed to logout even if the server request fails
            } finally {
                this.user = null;
                this.isAuthenticated = false;
                this.accessToken = null;
                router.push({ name: 'WelcomePage' });
                console.log('Logout successful.');
            }
        },

        async register(userData) {
            try {
                const response = await axiosInstance.post('/employees/register/', userData);
                if (response.status === 201) {
                    // Registration successful, redirect to sign-in page which is in the WelcomePage
                    router.push({ name: 'WelcomePage' });
                } else {
                    console.error('Registration failed:', response.data.error || 'Unknown error');
                    throw new Error(response.data.error || 'Registration failed');
                }
            } catch (error) {
                console.error('Error during registration:', error.response?.data || error.message);
                throw error;
            }
        },

        async fetchUser() {
            try {
                const response = await axiosInstance.get('/employees/user/');
                if (response.status === 200) {
                    this.user = response.data;
                    this.isAuthenticated = true;
                    // console.log('User fetched:', this.user);
                } else {
                    this.isAuthenticated = false;
                    this.user = null;
                    this.accessToken = null;
                    console.error('Failed to fetch user data:', response.data);
                }
            } catch (error) {
                console.error('Error fetching user:', error.response?.data || error.message);
                this.isAuthenticated = false;
                this.user = null;
                this.accessToken = null;
            }
        },

        async refreshAccessToken() {
            try {
                const response = await axiosInstance.post('/token/refresh/');
                if (response.data.success && response.data.access) {
                    this.accessToken = response.data.access;
                    this.isAuthenticated = true;
                    console.log('Access token refreshed.');
                } else {
                    this.isAuthenticated = false;
                    this.user = null;
                    this.accessToken = null;
                    console.error('Failed to refresh access token:', response.data.message);
                }
            } catch (error) {
                console.error('Failed to refresh access token:', error.response?.data || error.message);
                this.isAuthenticated = false;
                this.user = null;
                this.accessToken = null;
                router.push({ name: 'WelcomePage' });
            }
        },
    },
});
