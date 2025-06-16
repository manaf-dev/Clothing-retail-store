# Clothing Retail Store Management System

A comprehensive full-stack e-commerce and point-of-sale (POS) system built with Django REST Framework and Vue.js. This system provides complete retail store management including inventory tracking, sales processing, customer management, and reporting.

## 🚀 Features

### Core Functionality

- **Product Management**: Add, edit, and categorize products with images and variants
- **Inventory Management**: Real-time stock tracking and low-stock alerts
- **Point of Sale (POS)**: Complete checkout system with receipt generation
- **Order Management**: Process orders, track status, and manage fulfillment
- **Customer Management**: Customer profiles, purchase history, and loyalty tracking
- **Sales Reporting**: Comprehensive analytics and sales reports
- **Staff Management**: Role-based access control and staff tracking
- **Category Management**: Organize products into hierarchical categories

### Technical Features

- RESTful API with Django REST Framework
- Modern responsive UI with Vue.js 3 and Tailwind CSS
- Real-time inventory synchronization
- Image upload and management
- Advanced filtering and search
- Data export capabilities
- Automated data population for testing

## 📋 Requirements

### Backend Requirements

- Python 3.10+
- MySQL 5.7+ or 8.0+
- pip (Python package manager)

### Frontend Requirements

- Node.js 16+
- npm or yarn

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/manaf-dev/Clothing-retail-store.git
cd Clothing-retail-store
```

### 2. Backend Setup

#### Activate virtual environment

It is recommended to use a Python virtual environment to manage dependencies.

Create and activate a virtual environment:

```bash
# Create a virtual environment (if not already created)
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

Once activated, you can proceed to install the required dependencies.

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DB_NAME=clothing_store
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Database Setup

1. Create MySQL database:

```sql
CREATE DATABASE clothing_store;
```

2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:

```bash
python manage.py createsuperuser
```

#### Populate Sample Data (Optional)

```bash
# Option 1: Use management command (recommended)
python manage.py populate_sample_data

# Option 2: Use standalone script
python populate_data.py

# Option 3: Populate only products
python manage.py populate_products
```

#### Start Backend Server

```bash
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Environment Configuration

Create frontend environment file if needed (API base URL is configured in `src/services/api.js`).

#### Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 📁 Project Structure

```
Clothing-retail-store/
├── backend/                          # Django REST API Backend
│   ├── manage.py                     # Django management script
│   ├── populate_data.py             # Standalone data population script
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── apps/                        # Django applications
│   │   ├── authentication/          # User authentication & JWT
│   │   ├── categories/              # Product categories management
│   │   ├── customers/               # Customer management
│   │   ├── dashboard/               # Dashboard analytics
│   │   ├── inventory/               # Inventory tracking
│   │   ├── orders/                  # Order processing
│   │   ├── products/                # Product management
│   │   └── staff/                   # Staff management
│   ├── media/                       # Uploaded files (product images)
│   │   └── products/
│   └── store_backend/               # Django project settings
│       ├── settings.py              # Main configuration
│       ├── urls.py                  # URL routing
│       └── wsgi.py                  # WSGI application
├── frontend/                        # Vue.js Frontend
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── src/
│   │   ├── components/              # Vue components
│   │   │   ├── customers/           # Customer management UI
│   │   │   ├── dashboard/           # Dashboard components
│   │   │   ├── inventory/           # Inventory management UI
│   │   │   ├── layouts/             # Layout components
│   │   │   ├── pos/                 # Point of Sale UI
│   │   │   ├── products/            # Product management UI
│   │   │   ├── reports/             # Reporting components
│   │   │   └── sales/               # Sales management UI
│   │   ├── router/                  # Vue Router configuration
│   │   ├── services/                # API services and utilities
│   │   ├── stores/                  # State management (Pinia/Vuex)
│   │   ├── utils/                   # Utility functions
│   │   └── views/                   # Page components
│   └── public/                      # Static assets
└── README.md                        # This file
```

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token

### Products

- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

### Categories

- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Orders

- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order
- `DELETE /api/orders/{id}/` - Delete order

### Customers

- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Inventory

- `GET /api/inventory/` - List inventory records
- `POST /api/inventory/` - Create inventory record
- `GET /api/inventory/{id}/` - Get inventory details
- `PUT /api/inventory/{id}/` - Update inventory
- `DELETE /api/inventory/{id}/` - Delete inventory record

### Staff

- `GET /api/staff/` - List all staff members
- `POST /api/staff/` - Create new staff member
- `GET /api/staff/{id}/` - Get staff details
- `PUT /api/staff/{id}/` - Update staff
- `DELETE /api/staff/{id}/` - Delete staff member

### Dashboard & Reports

- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/dashboard/sales-chart/` - Sales chart data
- `GET /api/dashboard/top-products/` - Top selling products

## 🗃️ Database Models

### Core Models

#### Product

- Fields: name, description, price, cost_price, sku, category, image, is_active
- Relationships: belongs to Category, has many OrderItems, has many InventoryRecords

#### Category

- Fields: name, description, parent, is_active
- Relationships: has many Products, self-referential (parent/children)

#### Order

- Fields: order_number, customer, staff, total_amount, status, payment_method, order_date
- Relationships: belongs to Customer and Staff, has many OrderItems

#### Customer

- Fields: first_name, last_name, email, phone, address, date_joined
- Relationships: has many Orders

#### Inventory

- Fields: product, quantity_in_stock, minimum_stock_level, last_updated
- Relationships: belongs to Product

#### Staff

- Fields: user, role, hire_date, is_active
- Relationships: belongs to User, has many Orders

#### Port Conflicts

- Backend default port: 8000
- Frontend default port: 5173
- Use different ports if conflicts occur
