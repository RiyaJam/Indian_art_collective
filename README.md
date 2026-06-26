# 🎨 Indian Art Collective
## A Centralized Platform for Digital Representation of Indian Artisans

A complete full-stack DBMS mini project built with Flask + MySQL + Vanilla JS.

---

## 🚀 Quick Setup (Windows / VS Code)

### Prerequisites
- Python 3.9+ installed
- MySQL 8.0+ installed and running
- VS Code (recommended)

### Step 1 — Database Setup
```sql
-- Open MySQL Workbench or MySQL CLI and run:
source database/schema.sql
```

### Step 2 — Configure Backend
Edit `backend/config.py`:
```python
MYSQL_USER     = 'root'       # your MySQL username
MYSQL_PASSWORD = 'root'       # your MySQL password
MYSQL_DB       = 'indian_art_collective'
```

### Step 3 — Install Python Dependencies
```bash
cd indian_art_collective
pip install -r requirements.txt
```

### Step 4 — Run the Backend
```bash
cd backend
python app.py
```
Flask runs at: **http://localhost:5000**

### Step 5 — Open Frontend
Open `frontend/index.html` in a browser (or use VS Code Live Server).

---

## 👤 Demo Credentials

| Role     | Username / Email         | Password      |
|----------|--------------------------|---------------|
| Admin    | `admin`                  | `password123` |
| Artisan  | `sunita@artisan.com`     | `password123` |
| Artisan  | `ramesh@artisan.com`     | `password123` |
| Buyer    | `arjun@buyer.com`        | `password123` |
| Buyer    | `meera@buyer.com`        | `password123` |

---

## 📁 Project Structure
```
indian_art_collective/
├── backend/
│   ├── app.py               # Flask entry point
│   ├── config.py            # Configuration
│   ├── db.py                # MySQL connection
│   ├── models/              # Database models
│   ├── routes/              # API blueprints
│   ├── static/uploads/      # Uploaded images
│   └── utils/               # Auth + helpers
├── frontend/
│   ├── index.html           # Home page
│   ├── login_*.html         # Login pages (3 roles)
│   ├── dashboard_*.html     # Dashboards (3 roles)
│   ├── products.html        # Product listing + detail
│   ├── exhibitions.html     # Exhibitions (public)
│   ├── orders.html          # Orders page
│   ├── css/style.css        # Global styles
│   └── js/                  # api.js + utils.js
└── database/schema.sql      # Full schema + sample data
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint                      | Description          |
|--------|-------------------------------|----------------------|
| POST   | `/api/auth/login/admin`       | Admin login          |
| POST   | `/api/auth/login/artisan`     | Artisan login        |
| POST   | `/api/auth/login/buyer`       | Buyer login          |
| POST   | `/api/auth/register/artisan`  | Register artisan     |
| POST   | `/api/auth/register/buyer`    | Register buyer       |

### Products
| Method | Endpoint                      | Description          |
|--------|-------------------------------|----------------------|
| GET    | `/api/products`               | List (filter/search) |
| GET    | `/api/products/featured`      | Featured products    |
| GET    | `/api/products/:id`           | Product detail       |
| GET    | `/api/products/artisan/:id`   | Artisan's products   |
| POST   | `/api/products`               | Create product       |
| PUT    | `/api/products/:id`           | Update product       |
| DELETE | `/api/products/:id`           | Delete product       |

### Orders, Artisans, Buyers, Exhibitions, Schemes — full CRUD via REST

### Admin
| Method | Endpoint                      | Description          |
|--------|-------------------------------|----------------------|
| GET    | `/api/admin/dashboard`        | Full stats           |
| GET    | `/api/admin/export/artisans`  | CSV export           |
| GET    | `/api/admin/export/orders`    | CSV export           |

---

## 🏗️ Database Tables
ARTISANS · CRAFT · PRODUCT · BUYER · ORDERS · GOVERNMENT_SCHEMES · EXHIBITION · SPECIALIZES · ENROLLED_IN · PARTICIPATES · ADMIN

## 🔐 Role-Based Access
- **Admin**: Full CRUD on all tables, analytics, export
- **Artisan**: Manage own products, view own orders/schemes/exhibitions
- **Buyer**: Browse products, place orders, view exhibitions

