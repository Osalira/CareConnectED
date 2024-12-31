// src/utils/axiosInstance.js

import axios from 'axios';
import { useAuthStore } from '@/store/auth';
import router from '@/router';

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'https://careconnected-backend-v1-0.onrender.com/api',
    withCredentials: false, // JWTs are sent via headers, not cookies
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

        // If Unauthorized, attempt to refresh the token
        if (error.response && error.response.status === 401 && authStore.refreshToken) {
            try {
                const response = await axios.post(`${axiosInstance.defaults.baseURL}/token/refresh/`, {
                    refresh: authStore.refreshToken,
                });
                authStore.accessToken = response.data.access;
                // Retry the original request with the new access token
                error.config.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
                return axiosInstance(error.config);
            } catch (refreshError) {
                // Refresh token is invalid or expired, logout the user
                authStore.logout();
                router.push({ name: 'WelcomePage' });
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
