// ============================================================
// API Client — Indian Art Collective
// ============================================================

const API_BASE = 'http://localhost:5000';

const api = {
  token: () => localStorage.getItem('iac_token'),
  user:  () => JSON.parse(localStorage.getItem('iac_user') || 'null'),

  headers(json = true) {
    const h = {};
    if (json) h['Content-Type'] = 'application/json';
    const t = this.token();
    if (t) h['Authorization'] = `Bearer ${t}`;
    return h;
  },

  async request(method, path, body = null, formData = false) {
    const opts = { method, headers: this.headers(!formData) };
    if (body) opts.body = formData ? body : JSON.stringify(body);
    try {
      const res = await fetch(`${API_BASE}${path}`, opts);
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || `Error ${res.status}`);
      return data;
    } catch (err) {
      throw err;
    }
  },

  get:    (path)       => api.request('GET',    path),
  post:   (path, body) => api.request('POST',   path, body),
  put:    (path, body) => api.request('PUT',    path, body),
  delete: (path)       => api.request('DELETE', path),
  upload: (path, fd)   => api.request('POST',   path, fd, true),

  // Auth
  loginAdmin:   (d) => api.post('/api/auth/login/admin',   d),
  loginArtisan: (d) => api.post('/api/auth/login/artisan', d),
  loginBuyer:   (d) => api.post('/api/auth/login/buyer',   d),
  registerArtisan: (d) => api.post('/api/auth/register/artisan', d),
  registerBuyer:   (d) => api.post('/api/auth/register/buyer',   d),

  // Stats
  stats: () => api.get('/api/stats'),

  // Products
  products: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get('/api/products' + (q ? '?' + q : ''));
  },
  product:       (id) => api.get(`/api/products/${id}`),
  featuredProducts: () => api.get('/api/products/featured'),
  artisanProducts:  (id) => api.get(`/api/products/artisan/${id}`),
  createProduct:    (fd)  => api.upload('/api/products', fd),
  updateProduct:    (id, fd) => {
    const opts = { method: 'PUT', headers: api.headers(false) };
    opts.body = fd;
    return fetch(`${API_BASE}/api/products/${id}`, opts).then(r => r.json());
  },
  deleteProduct:    (id) => api.delete(`/api/products/${id}`),

  // Artisans
  artisans:     ()   => api.get('/api/artisans'),
  artisan:      (id) => api.get(`/api/artisans/${id}`),
  artisanStats: (id) => api.get(`/api/artisans/${id}/stats`),
  artisanSchemes:    (id) => api.get(`/api/artisans/${id}/schemes`),
  artisanExhibitions:(id) => api.get(`/api/artisans/${id}/exhibitions`),
  updateArtisan: (id, d) => api.put(`/api/artisans/${id}`, d),
  deleteArtisan: (id)    => api.delete(`/api/artisans/${id}`),

  // Buyers
  buyers:       ()   => api.get('/api/buyers'),
  buyer:        (id) => api.get(`/api/buyers/${id}`),
  updateBuyer:  (id, d) => api.put(`/api/buyers/${id}`, d),
  deleteBuyer:  (id)    => api.delete(`/api/buyers/${id}`),
  buyerOrders:  (id) => api.get(`/api/orders/buyer/${id}`),

  // Orders
  orders:       ()   => api.get('/api/orders'),
  order:        (id) => api.get(`/api/orders/${id}`),
  artisanOrders:(id) => api.get(`/api/orders/artisan/${id}`),
  placeOrder:   (d)  => api.post('/api/orders', d),
  deleteOrder:  (id) => api.delete(`/api/orders/${id}`),

  // Exhibitions
  exhibitions:  ()   => api.get('/api/exhibitions'),
  exhibition:   (id) => api.get(`/api/exhibitions/${id}`),
  createExhibition: (d) => api.post('/api/exhibitions', d),
  updateExhibition: (id, d) => api.put(`/api/exhibitions/${id}`, d),
  deleteExhibition: (id) => api.delete(`/api/exhibitions/${id}`),
  assignArtisanExhibition: (exId, artisanId) => api.post(`/api/exhibitions/${exId}/assign`, { artisan_id: artisanId }),
  removeArtisanExhibition: (exId, artisanId) => api.post(`/api/exhibitions/${exId}/remove-artisan`, { artisan_id: artisanId }),

  // Schemes
  schemes:      ()   => api.get('/api/schemes'),
  scheme:       (id) => api.get(`/api/schemes/${id}`),
  createScheme: (d)  => api.post('/api/schemes', d),
  updateScheme: (id, d) => api.put(`/api/schemes/${id}`, d),
  deleteScheme: (id)    => api.delete(`/api/schemes/${id}`),
  enrollArtisan:  (schemeId, artisanId) => api.post(`/api/schemes/${schemeId}/enroll`, { artisan_id: artisanId }),
  unenrollArtisan:(schemeId, artisanId) => api.post(`/api/schemes/${schemeId}/unenroll`, { artisan_id: artisanId }),

  // Admin
  adminDashboard: () => api.get('/api/admin/dashboard'),
  crafts:       ()   => api.get('/api/admin/crafts'),
  createCraft:  (d)  => api.post('/api/admin/crafts', d),
  updateCraft:  (id, d) => api.put(`/api/admin/crafts/${id}`, d),
  deleteCraft:  (id)    => api.delete(`/api/admin/crafts/${id}`),
};

// Auth helpers
function saveAuth(data) {
  localStorage.setItem('iac_token', data.token);
  localStorage.setItem('iac_user', JSON.stringify({ id: data.id, name: data.name, role: data.role }));
}

function clearAuth() {
  localStorage.removeItem('iac_token');
  localStorage.removeItem('iac_user');
}

function requireAuth(role = null) {
  const user = api.user();
  if (!user || !api.token()) {
    window.location.href = `/login_${role || 'buyer'}.html`;
    return null;
  }
  if (role && user.role !== role) {
    window.location.href = `/login_${user.role}.html`;
    return null;
  }
  return user;
}

function redirectIfLoggedIn() {
  const user = api.user();
  if (user && api.token()) {
    window.location.href = `/dashboard_${user.role}.html`;
  }
}
