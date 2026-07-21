import axios from 'axios';

const API_BASE_URL = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const api = {
  // Auth
  async register(name, email, password, phone) {
    const res = await client.post('/api/auth/register', { name, email, password, phone });
    return res.data;
  },
  async login(email, password) {
    const res = await client.post('/api/auth/login', { email, password });
    if (res.data && res.data.data && res.data.data.access_token) {
      localStorage.setItem('token', res.data.data.access_token);
    }
    return res.data;
  },
  async getMe() {
    const res = await client.get('/api/auth/me');
    return res.data;
  },
  logout() {
    localStorage.removeItem('token');
  },

  // Cars
  async getCars(params = {}) {
    const res = await client.get('/api/cars', { params });
    return res.data;
  },
  async getCar(id) {
    const res = await client.get(`/api/cars/${id}`);
    return res.data;
  },

  // Showrooms
  async getNearbyShowrooms(lat, lng, radius = 50) {
    const res = await client.get('/api/showrooms/nearby', {
      params: { lat, lng, radius }
    });
    return res.data;
  },
  async getShowroomInventory(showroom_id) {
    const res = await client.get(`/api/showrooms/${showroom_id}/availability`);
    return res.data;
  },

  // AI & RAG
  async chatAI(message, history = []) {
    const res = await client.post('/api/ai/chat', { message, history });
    return res.data;
  },
  async recommendAI(preferences) {
    const res = await client.post('/api/ai/recommend', preferences);
    return res.data;
  },
  async compareAI(car_ids, aspect = null) {
    const res = await client.post('/api/ai/compare', { car_ids, aspect });
    return res.data;
  },

  // Reviews & Wishlist
  async getReviews(car_id) {
    const res = await client.get(`/api/reviews/car/${car_id}`);
    return res.data;
  },
  async addReview(car_id, rating, comment) {
    const res = await client.post('/api/reviews', { car_id, rating, comment });
    return res.data;
  },
  async getWishlist() {
    const res = await client.get('/api/wishlist');
    return res.data;
  },
  async toggleWishlist(car_id) {
    const res = await client.post(`/api/wishlist?car_id=${car_id}`);
    return res.data;
  },

  // Bookings
  async createBooking(car_id, showroom_id, booking_type, scheduled_date) {
    const res = await client.post('/api/bookings', {
      car_id,
      showroom_id,
      booking_type,
      scheduled_date
    });
    return res.data;
  }
};
