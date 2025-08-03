import axios from 'axios';

// Use localhost for development
const API_BASE_URL = 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Categories API
export const categoriesAPI = {
  getAll: () => api.get('/categories'),
  getById: (id) => api.get(`/categories/${id}`),
  getProducts: (id, page = 1, limit = 12) => api.get(`/categories/${id}/products?page=${page}&limit=${limit}`),
};

// Products API
export const productsAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return api.get(`/products?${queryParams.toString()}`);
  },
  getById: (id) => api.get(`/products/${id}`),
  getFeatured: () => api.get('/products/featured'),
  getNew: () => api.get('/products/new'),
  getTrending: () => api.get('/products/trending'),
  search: (query, params = {}) => {
    const queryParams = new URLSearchParams({ q: query });
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return api.get(`/products/search?${queryParams.toString()}`);
  },
};

// Sellers API
export const sellersAPI = {
  getAll: () => api.get('/sellers'),
  getById: (id) => api.get(`/sellers/${id}`),
  getProducts: (id, page = 1, limit = 12) => api.get(`/sellers/${id}/products?page=${page}&limit=${limit}`),
};

// Reviews API
export const reviewsAPI = {
  getProductReviews: (productId) => api.get(`/reviews/products/${productId}`),
  createReview: (productId, reviewData) => api.post(`/reviews/products/${productId}`, reviewData),
  markHelpful: (reviewId) => api.put(`/reviews/reviews/${reviewId}/helpful`),
  deleteReview: (reviewId) => api.delete(`/reviews/reviews/${reviewId}`),
};

// Generic API utilities
export const apiUtils = {
  handleError: (error) => {
    if (error.response) {
      // Server responded with error status
      return {
        message: error.response.data?.message || 'حدث خطأ في الخادم',
        status: error.response.status,
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'لا يمكن الاتصال بالخادم',
        status: 0,
      };
    } else {
      // Something else happened
      return {
        message: error.message || 'حدث خطأ غير متوقع',
        status: -1,
      };
    }
  },
};

export default api;