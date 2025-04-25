# Bluestock Backend

This is the backend implementation for the Bluestock platform, featuring a customized admin panel and data management interfaces.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Features

- Customized Django admin interface
- Bulk operations for data management
- Administrator dashboard views
- Data export functionality
- Role-based permissions system 