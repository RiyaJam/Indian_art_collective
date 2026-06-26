// ============================================================
// Indian Art Collective — Global JS Utilities
// ============================================================

const API_BASE = 'http://localhost:5000';

// ── Auth Storage ─────────────────────────────────────────────
const Auth = {
  save(token, role, name, id) {
    localStorage.setItem('iac_token', token);
    localStorage.setItem('iac_role', role);
    localStorage.setItem('iac_name', name);
    localStorage.setItem('iac_id', id);
  },
  getToken() { return localStorage.getItem('iac_token'); },
  getRole() { return localStorage.getItem('iac_role'); },
  getName() { return localStorage.getItem('iac_name'); },
  getId() { return parseInt(localStorage.getItem('iac_id')); },
  isLoggedIn() { return !!this.getToken(); },
  clear() { ['iac_token','iac_role','iac_name','iac_id'].forEach(k => localStorage.removeItem(k)); },
  logout() { this.clear(); window.location.href = '../frontend/index.html'; },
  requireRole(role) {
    if (!this.isLoggedIn() || this.getRole() !== role) {
      window.location.href = 'index.html';
    }
  }
};

// ── API Fetch Wrapper ─────────────────────────────────────────
async function apiFetch(endpoint, options = {}) {
  const token = Auth.getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  // Don't set Content-Type for FormData
  if (options.body instanceof FormData) delete headers['Content-Type'];

  try {
    const res = await fetch(API_BASE + endpoint, { ...options, headers });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw { status: res.status, message: data.error || 'Request failed' };
    return data;
  } catch (err) {
    if (err.status === 401) { Auth.logout(); }
    throw err;
  }
}

// ── Toast Notifications ───────────────────────────────────────
function showToast(message, type = 'success', duration = 3000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  const colors = { success: '#2E7D52', error: '#C0392B', info: '#2D3E8B', warning: '#8B6914' };
  toast.style.cssText = `background:${colors[type]||colors.success};color:white;padding:.75rem 1.2rem;border-radius:8px;font-family:'Crimson Pro',serif;font-size:.95rem;box-shadow:0 4px 20px rgba(0,0,0,.2);animation:slideIn .3s ease;max-width:320px;`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity .3s'; setTimeout(() => toast.remove(), 300); }, duration);
}

// ── Loading State ─────────────────────────────────────────────
function setLoading(btn, loading, text = '') {
  if (!btn) return;
  if (loading) { btn.disabled = true; btn._orig = btn.textContent; btn.textContent = text || 'Loading...'; }
  else { btn.disabled = false; btn.textContent = btn._orig || text; }
}

// ── Format Helpers ────────────────────────────────────────────
function formatCurrency(amount) {
  return '₹' + parseFloat(amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}
function truncate(str, len = 80) { return str && str.length > len ? str.slice(0, len) + '…' : str || ''; }
function avatarInitials(name) { return (name || 'U').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase(); }

// ── Navbar Setup ──────────────────────────────────────────────
function initNavbar() {
  const name = Auth.getName();
  const role = Auth.getRole();
  const userEl = document.getElementById('navbar-user');
  if (!userEl) return;
  if (name) {
    const dashLinks = { admin: 'dashboard_admin.html', artisan: 'dashboard_artisan.html', buyer: 'dashboard_buyer.html' };
    userEl.innerHTML = `
      <a href="${dashLinks[role] || '#'}" class="navbar-avatar" title="Dashboard">${avatarInitials(name)}</a>
      <span style="color:rgba(255,255,255,.65);font-size:.85rem">${name}</span>
      <button onclick="Auth.logout()" class="btn btn-sm btn-ghost" style="color:rgba(255,255,255,.65);border-color:rgba(255,255,255,.2)">Logout</button>
    `;
  } else {
    userEl.innerHTML = `<a href="login_buyer.html" class="btn btn-sm btn-outline" style="border-color:var(--saffron);color:var(--saffron)">Login</a>`;
  }
}

// ── Pagination ────────────────────────────────────────────────
function renderPagination(containerId, currentPage, totalPages, onPageChange) {
  const container = document.getElementById(containerId);
  if (!container || totalPages <= 1) { if (container) container.innerHTML = ''; return; }
  let html = `<button class="page-btn" onclick="(${onPageChange})(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>‹</button>`;
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
      html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="(${onPageChange})(${i})">${i}</button>`;
    } else if (i === currentPage - 3 || i === currentPage + 3) {
      html += `<span style="padding:0 .3rem;color:var(--muted)">…</span>`;
    }
  }
  html += `<button class="page-btn" onclick="(${onPageChange})(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>›</button>`;
  container.innerHTML = html;
}

// ── Modal Helpers ─────────────────────────────────────────────
function openModal(id) { const m = document.getElementById(id); if (m) { m.style.display = 'flex'; m.classList.add('fade-in'); } }
function closeModal(id) { const m = document.getElementById(id); if (m) m.style.display = 'none'; }
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) e.target.style.display = 'none';
});

// ── Confirm Dialog ────────────────────────────────────────────
function confirmAction(message, onConfirm) {
  if (confirm(message)) onConfirm();
}

// ── Image Preview ─────────────────────────────────────────────
function setupImagePreview(inputId, previewId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  if (!input || !preview) return;
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => { preview.src = e.target.result; preview.classList.remove('hidden'); };
      reader.readAsDataURL(file);
    }
  });
}

// ── Sidebar Active Link ───────────────────────────────────────
function setSidebarActive() {
  const page = window.location.pathname.split('/').pop();
  document.querySelectorAll('.sidebar-menu a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
}

// ── Chart helpers (using Canvas) ─────────────────────────────
function drawBarChart(canvasId, labels, values, color = '#C4622D') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  const pad = { top: 20, right: 20, bottom: 40, left: 60 };
  const maxVal = Math.max(...values, 1);
  const barW = (w - pad.left - pad.right) / labels.length;

  ctx.clearRect(0, 0, w, h);
  // Grid lines
  ctx.strokeStyle = '#F0E4CE'; ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + (h - pad.top - pad.bottom) * i / 4;
    ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
    ctx.fillStyle = '#8A7060'; ctx.font = '11px DM Mono,monospace';
    ctx.fillText(Math.round(maxVal * (4 - i) / 4), 4, y + 4);
  }
  // Bars
  values.forEach((val, i) => {
    const x = pad.left + i * barW;
    const barH = (val / maxVal) * (h - pad.top - pad.bottom);
    const y = h - pad.bottom - barH;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(x + barW * .15, y, barW * .7, barH, [3, 3, 0, 0]) : ctx.rect(x + barW * .15, y, barW * .7, barH);
    ctx.fill();
    // Label
    ctx.fillStyle = '#3D2B1A'; ctx.font = '10px DM Mono,monospace';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], x + barW / 2, h - pad.bottom + 15);
  });
}

function drawDonutChart(canvasId, labels, values, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const cx = canvas.width / 2, cy = canvas.height / 2;
  const r = Math.min(cx, cy) - 30, inner = r * 0.55;
  const total = values.reduce((a, b) => a + b, 0) || 1;
  let angle = -Math.PI / 2;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  values.forEach((val, i) => {
    const slice = (val / total) * Math.PI * 2;
    ctx.beginPath(); ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, r, angle, angle + slice);
    ctx.closePath(); ctx.fillStyle = colors[i % colors.length]; ctx.fill();
    angle += slice;
  });
  // Inner circle (donut hole)
  ctx.beginPath(); ctx.arc(cx, cy, inner, 0, Math.PI * 2);
  ctx.fillStyle = 'white'; ctx.fill();
  // Center text
  ctx.fillStyle = '#1A1209'; ctx.font = 'bold 20px DM Mono,monospace'; ctx.textAlign = 'center';
  ctx.fillText(total, cx, cy + 2);
  ctx.fillStyle = '#8A7060'; ctx.font = '11px Crimson Pro,serif';
  ctx.fillText('total', cx, cy + 18);

  // Legend
  const legendY = canvas.height - 10;
  labels.forEach((label, i) => {
    const lx = 10 + i * (canvas.width / labels.length);
    ctx.fillStyle = colors[i % colors.length];
    ctx.fillRect(lx, legendY - 8, 10, 10);
    ctx.fillStyle = '#3D2B1A'; ctx.font = '10px Crimson Pro,serif'; ctx.textAlign = 'left';
    ctx.fillText(truncate(label, 10), lx + 14, legendY);
  });
}

// ── Init ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  setSidebarActive();
});
