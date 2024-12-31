// src/utils/axiosInstance.js

import axios from 'axios';
import { useAuthStore } from '@/store/auth';
import router from '@/router';

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'https://careconnected-backend-v1-0.onrender.com/api',
    withCredentials: true, // Enable sending cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor to Attach Access Token
axiosInstance.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore();
        if (authStore.accessToken) {
            config.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor to Handle Token Refresh
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore();

        // If Unauthorized and not already trying to retry
        if (error.response && error.response.status === 401 && !error.config.__isRetryRequest) {
            error.config.__isRetryRequest = true;
            try {
                await authStore.refreshAccessToken();
                // Retry the original request with the new access token
                return axiosInstance(error.config);
            } catch (refreshError) {
                // Refresh token is invalid or expired, logout the user
                await authStore.logout();
                router.push({ name: 'SignInPage' });
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
