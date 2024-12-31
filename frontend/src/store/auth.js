// src/store/auth.js

import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axiosInstance';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
        accessToken: null,
        refreshToken: localStorage.getItem('refreshToken') || null, // Persisted
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
                    this.refreshToken = response.data.refresh;
                    localStorage.setItem('refreshToken', this.refreshToken); // Persist
                    // console.log("refreshed osa token:", this.refreshToken);
                    // console.log('Login successful:', this.user);
                    router.push({ name: 'HomePage' });
                } else {
                    this.isAuthenticated = false;
                    this.user = null;
                    this.accessToken = null;
                    this.refreshToken = null;
                    localStorage.removeItem('refreshToken'); // Remove if exists
                    console.error('Login failed:', response.data.message);
                }
            } catch (error) {
                console.error('Error during login:', error.response?.data || error.message);
                throw error;
            }
        },

        async logout() {
            try {
                if (this.refreshToken) {
                    // Send refresh token to blacklist it
                    await axiosInstance.post('/employees/logout/', {
                        refresh: this.refreshToken,
                    });
                }
            } catch (error) {
                console.error('Error during logout:', error.response?.data || error.message);
                // Proceed to logout even if the server request fails
            } finally {
                this.user = null;
                this.isAuthenticated = false;
                this.accessToken = null;
                this.refreshToken = null;
                localStorage.removeItem('refreshToken'); // Remove persisted token
                router.push({ name: 'WelcomePage' });
                console.log('Logout successful.');
            }
        },

        async register(userData) {
            try {
                const response = await axiosInstance.post('/employees/register/', userData);
                if (response.status === 201) {
                    // Registration successful, redirect to sign-in page
                    router.push({ name: 'SignInPage' });
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
            if (!this.isAuthenticated) return;
            try {
                const response = await axiosInstance.get('/employees/user/');
                if (response.status === 200) {
                    this.user = response.data;
                    this.isAuthenticated = true;
                    console.log('User fetched:', this.user);
                } else {
                    this.isAuthenticated = false;
                    this.user = null;
                    this.accessToken = null;
                    this.refreshToken = null;
                    localStorage.removeItem('refreshToken');
                    console.error('Failed to fetch user data:', response.data);
                }
            } catch (error) {
                console.error('Error fetching user:', error.response?.data || error.message);
                this.isAuthenticated = false;
                this.user = null;
                this.accessToken = null;
                this.refreshToken = null;
                localStorage.removeItem('refreshToken');
            }
        },

        async refreshAccessToken() {
            if (!this.refreshToken) {
                this.logout();
                return;
            }
            try {
                const response = await axiosInstance.post('/token/refresh/', {
                    refresh: this.refreshToken,  
                });
                this.accessToken = response.data.access;
                // console.log('Access token refreshed.', this.accessToken);
            } catch (error) {
                console.error('Failed to refresh access token:', error.response?.data || error.message);
                this.logout();
            }
        },
    },
});
