# Inventory Management System

A backend-focused inventory management system built with **FastAPI**, featuring **JWT authentication, role-based access control (RBAC), warehouse management, real-time stock updates, and transaction-safe inventory operations**.

This project demonstrates **production-style backend architecture** including service layers, database transactions, and concurrency handling.

---

# Tech Stack

### Backend

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic (Database migrations)
* JWT Authentication
* Role-Based Access Control (RBAC)
* WebSockets for real-time updates

### Frontend

* Streamlit

---

# Features

### Authentication

* JWT access tokens
* Refresh tokens
* Secure password hashing using bcrypt

### Role-Based Access Control

Three user roles:

* **Admin**
* **Manager**
* **Viewer**

Permissions are enforced through dependency-based authorization.

---

### Warehouse Management

Admins can:

* Create warehouses
* Assign managers to warehouses

Managers can only manage **assigned warehouses**.

---

### Inventory Management

Admins can:

* Create inventory items
* Manage categories

Managers can:

* Update stock

All stock changes are stored as **inventory movement history**.

---

### Stock Movement Tracking

Every stock update generates a movement record.

Movement types:

```
IN
OUT
ADJUST
```

This allows **full audit history of inventory changes**.

---

### Concurrency-Safe Stock Updates

Stock updates use **database row locking**:

```
SELECT ... FOR UPDATE
```

This prevents race conditions when multiple users update stock simultaneously.

Example problem avoided:

```
Manager A reads stock = 100
Manager B reads stock = 100

Both add 10

Without locking → final = 110 ❌  
With locking → final = 120 ✅
```

---

### Real-Time Inventory Updates

Stock changes are broadcast via **WebSockets** to connected clients.

This allows dashboards to update automatically without refreshing.

---

# System Architecture

```
Streamlit UI
      │
      ▼
FastAPI API Layer
      │
      ▼
Service Layer (Business Logic)
      │
      ▼
SQLAlchemy ORM
      │
      ▼
PostgreSQL Database
```

---

# API Overview

### Authentication

```
POST /auth/register
POST /auth/login
```

---

### Items

```
POST /items/
GET /items/items
DELETE /items/item/{item_id}
```

---

### Warehouses

```
POST /items/warehouse
GET /items/warehouse
POST /items/warehouse/{warehouse_id}/assign/{user_id}
```

---

### Inventory

```
POST /items/stock
GET /items/warehouse/{warehouse_id}
GET /items/movements
```

---

# Project Structure

```
inventory-management-system
│
├── backend
│   └── inventory_system
│       ├── api
│       ├── services
│       ├── models
│       ├── schemas
│       ├── core
│       ├── db
│       └── websocket
│
├── frontend
│   └── inventory_system_UI
│       ├── pages
│       └── app.py
│
└── README.md
```

---

# Setup Instructions

### 1. Clone repository

```
git clone <repo-url>
```

---

### 2. Start Backend

```
cd backend/inventory_system
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

### 3. Start Frontend

```
cd frontend/inventory_system_UI
python -m venv venv
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at:

```
http://localhost:8501
```

---

# Key Backend Concepts Demonstrated

* Service layer architecture
* JWT authentication
* RBAC authorization
* Database transactions
* Concurrency control
* Real-time systems with WebSockets
* Clean API design

---

# Future Improvements

* Redis caching
* Rate limiting
* Distributed inventory updates
* React frontend
* Background workers

---

# Author

Piyush Ranjan Jena
