// ============================================================
// Shared UI Utilities
// ============================================================

// Toast notifications
function showToast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || '•'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOutRight .3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Format currency
function formatCurrency(amount) {
  return '₹' + Number(amount).toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

// Format date
function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

// Debounce
function debounce(fn, delay = 350) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}

// Render navbar based on auth
function renderNavbar(activePage = '') {
  const user = api.user();
  const nav = document.getElementById('main-navbar');
  if (!nav) return;

  const links = [
    { href: 'index.html', label: 'Home', key: 'home' },
    { href: 'products.html', label: 'Products', key: 'products' },
    { href: 'exhibitions.html', label: 'Exhibitions', key: 'exhibitions' },
  ];

  let navLinks = links.map(l => `
    <li><a href="${l.href}" class="${activePage === l.key ? 'active' : ''}">${l.label}</a></li>
  `).join('');

  let actionBtns = '';
  if (user) {
    actionBtns = `
      <a href="dashboard_${user.role}.html" class="btn btn-secondary btn-sm">Dashboard</a>
      <button onclick="logout()" class="btn btn-ghost btn-sm">Logout</button>
    `;
  } else {
    actionBtns = `
      <a href="login_buyer.html" class="btn btn-secondary btn-sm">Login</a>
      <a href="login_buyer.html#register" class="btn btn-primary btn-sm">Register</a>
    `;
  }

  nav.innerHTML = `
    <div class="navbar-brand">
      <div class="logo-icon">🎨</div>
      <span>Indian Art Collective</span>
    </div>
    <ul class="navbar-nav">${navLinks}</ul>
    <div class="navbar-actions">${actionBtns}</div>
  `;
}

function logout() {
  clearAuth();
  window.location.href = 'index.html';
}

// Sidebar active link
function setActiveSidebarLink(key) {
  document.querySelectorAll('.sidebar-nav a').forEach(a => {
    a.classList.toggle('active', a.dataset.key === key);
  });
}

// Show/hide tab content
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(target)?.classList.add('active');
    });
  });
}

// Modal helpers
function openModal(id) {
  document.getElementById(id)?.classList.add('open');
}
function closeModal(id) {
  document.getElementById(id)?.classList.remove('open');
}

// Confirm dialog
function confirmAction(message, onConfirm) {
  if (confirm(message)) onConfirm();
}

// Render skill badge
function skillBadge(level) {
  const map = { Master: 'saffron', Advanced: 'jade', Intermediate: 'gold', Beginner: 'ruby' };
  return `<span class="badge badge-${map[level] || 'gold'}">${level}</span>`;
}

// Render product card HTML
function productCardHTML(p) {
  const img = p.Image_URL || '/static/uploads/default_product.jpg';
  return `
    <div class="card product-card" onclick="viewProduct(${p.Product_ID})">
      <div class="product-img">
        <img src="${img}" alt="${p.Product_Name}" onerror="this.src='https://placehold.co/400x300/FAF3E8/E8650A?text=Art'">
        ${p.Category ? `<span class="product-badge">${p.Category}</span>` : ''}
      </div>
      <div class="product-body">
        <div class="craft-tag">${p.Craft_Name || 'Handicraft'}</div>
        <div class="product-name">${p.Product_Name}</div>
        <div class="artisan-name">by ${p.Artisan_Name || 'Unknown Artisan'} · ${p.Region || p.Artisan_State || ''}</div>
        <div class="product-footer">
          <div>
            <div class="price">${formatCurrency(p.Price)}</div>
            ${p.Stock_Quantity <= 5 && p.Stock_Quantity > 0 ? `<div style="font-size:.72rem;color:var(--ruby)">Only ${p.Stock_Quantity} left</div>` : ''}
            ${p.Stock_Quantity === 0 ? `<div style="font-size:.72rem;color:var(--ruby)">Out of stock</div>` : ''}
          </div>
          <button class="btn btn-primary btn-sm" onclick="event.stopPropagation();addToCart(${p.Product_ID},'${p.Product_Name}',${p.Price})">
            🛒 Buy
          </button>
        </div>
      </div>
    </div>
  `;
}

function viewProduct(id) {
  window.location.href = `products.html?id=${id}`;
}

function addToCart(id, name, price) {
  const user = api.user();
  if (!user || user.role !== 'buyer') {
    showToast('Please login as a buyer to place orders', 'info');
    setTimeout(() => window.location.href = 'login_buyer.html', 1500);
    return;
  }
  // Open quick order modal or go to product page
  window.location.href = `products.html?id=${id}&buy=1`;
}

// Number counter animation
function animateCounter(el, target, duration = 1200) {
  const start = 0;
  const step = target / (duration / 16);
  let current = start;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.floor(current).toLocaleString('en-IN');
    if (current >= target) clearInterval(timer);
  }, 16);
}

// Simple bar chart using canvas
function drawBarChart(canvasId, labels, values, color = '#E8650A') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const pad = { top: 20, right: 20, bottom: 40, left: 60 };
  const max = Math.max(...values, 1);

  ctx.clearRect(0, 0, W, H);

  const barW = (W - pad.left - pad.right) / labels.length;

  values.forEach((v, i) => {
    const barH = ((v / max) * (H - pad.top - pad.bottom));
    const x = pad.left + i * barW + barW * .15;
    const y = H - pad.bottom - barH;
    const bw = barW * .7;

    // Bar
    const grad = ctx.createLinearGradient(0, y, 0, H - pad.bottom);
    grad.addColorStop(0, color);
    grad.addColorStop(1, color + '80');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.roundRect(x, y, bw, barH, [4, 4, 0, 0]);
    ctx.fill();

    // Label
    ctx.fillStyle = '#1A120999';
    ctx.font = '11px DM Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], x + bw / 2, H - pad.bottom + 16);

    // Value
    ctx.fillStyle = '#1A1209';
    ctx.font = '600 11px DM Sans, sans-serif';
    ctx.fillText(v.toLocaleString('en-IN'), x + bw / 2, y - 6);
  });

  // Y-axis line
  ctx.strokeStyle = '#E2D4C0';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, H - pad.bottom);
  ctx.stroke();
}

// Donut chart
function drawDonutChart(canvasId, labels, values, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const outerR = Math.min(W, H) / 2 - 10;
  const innerR = outerR * .55;
  const total = values.reduce((a, b) => a + b, 0) || 1;

  ctx.clearRect(0, 0, W, H);
  let angle = -Math.PI / 2;

  values.forEach((v, i) => {
    const slice = (v / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, outerR, angle, angle + slice);
    ctx.closePath();
    ctx.fillStyle = colors[i % colors.length];
    ctx.fill();
    angle += slice;
  });

  // Inner circle (donut hole)
  ctx.beginPath();
  ctx.arc(cx, cy, innerR, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.fill();

  // Center text
  ctx.fillStyle = '#1A1209';
  ctx.font = `900 ${Math.floor(outerR * .35)}px Playfair Display, serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(total.toLocaleString('en-IN'), cx, cy);
}
