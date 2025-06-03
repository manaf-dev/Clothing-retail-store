# Clothing Retail Store Backend

This is a Django backend for a clothing retail store management system. It uses MySQL as the database and python-decouple for environment variable management.

## Features

- Modular, scalable architecture
- REST API endpoints for products, categories, inventory, orders, customers, authentication, and staff management
- Environment variables managed via `.env` and `python-decouple`

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root (see `.env.example` for required variables).
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `store_backend/` - Django project root
- `apps/` - Django apps (to be created for products, orders, etc.)
- `.env` - Environment variables

## Requirements

- Python 3.8+
- MySQL

## License

MIT
