import axios from 'axios';

const ADMIN_API_BASE_URL = `${process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL}/api/admin`;

const adminApi = axios.create({
  baseURL: ADMIN_API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
adminApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
adminApi.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('admin_token');
      localStorage.removeItem('admin_info');
      window.location.href = '/admin/login';
    }
    console.error('Admin API Error:', error);
    return Promise.reject(error);
  }
);

// Authentication API
export const adminAuthAPI = {
  login: (credentials) => adminApi.post('/login', credentials),
  getProfile: () => adminApi.get('/profile'),
  changePassword: (passwordData) => adminApi.put('/change-password', passwordData),
  
  // Save auth data
  saveAuth: (token, adminInfo) => {
    localStorage.setItem('admin_token', token);
    localStorage.setItem('admin_info', JSON.stringify(adminInfo));
  },
  
  // Get auth data
  getAuth: () => {
    const token = localStorage.getItem('admin_token');
    const adminInfo = localStorage.getItem('admin_info');
    return {
      token,
      adminInfo: adminInfo ? JSON.parse(adminInfo) : null
    };
  },
  
  // Clear auth data
  clearAuth: () => {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_info');
  },
  
  // Check if logged in
  isLoggedIn: () => {
    return !!localStorage.getItem('admin_token');
  }
};

// Dashboard API
export const adminDashboardAPI = {
  getStats: () => adminApi.get('/dashboard/stats'),
  getAnalytics: () => adminApi.get('/analytics'),
};

// Orders API
export const adminOrdersAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return adminApi.get(`/orders?${queryParams.toString()}`);
  },
  getById: (id) => adminApi.get(`/orders/${id}`),
  update: (id, data) => adminApi.put(`/orders/${id}`, data),
  delete: (id) => adminApi.delete(`/orders/${id}`),
};

// Products API
export const adminProductsAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return adminApi.get(`/products?${queryParams.toString()}`);
  },
  create: (data) => adminApi.post('/products', data),
  update: (id, data) => adminApi.put(`/products/${id}`, data),
  delete: (id) => adminApi.delete(`/products/${id}`),
};

// Categories API  
export const adminCategoriesAPI = {
  getAll: () => adminApi.get('/categories'),
  create: (data) => adminApi.post('/categories', data),
  update: (id, data) => adminApi.put(`/categories/${id}`, data),
  delete: (id) => adminApi.delete(`/categories/${id}`),
};

// Sellers API
export const adminSellersAPI = {
  getAll: () => adminApi.get('/sellers'),
  approve: (id) => adminApi.put(`/sellers/${id}/approve`),
  reject: (id) => adminApi.put(`/sellers/${id}/reject`),
  update: (id, data) => adminApi.put(`/sellers/${id}`, data),
  delete: (id) => adminApi.delete(`/sellers/${id}`),
};

// Settings API
export const adminSettingsAPI = {
  get: () => adminApi.get('/settings'),
  update: (data) => adminApi.put('/settings', data),
};

// Notifications API
export const adminNotificationsAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return adminApi.get(`/notifications?${queryParams.toString()}`);
  },
  markAsRead: (id) => adminApi.put(`/notifications/${id}/read`),
  markAllAsRead: () => adminApi.put('/notifications/mark-all-read'),
};

// Generic error handler
export const adminApiUtils = {
  handleError: (error) => {
    if (error.response) {
      return {
        message: error.response.data?.detail || error.response.data?.message || 'حدث خطأ في الخادم',
        status: error.response.status,
      };
    } else if (error.request) {
      return {
        message: 'لا يمكن الاتصال بالخادم',
        status: 0,
      };
    } else {
      return {
        message: error.message || 'حدث خطأ غير متوقع',
        status: -1,
      };
    }
  },
};

export default adminApi;